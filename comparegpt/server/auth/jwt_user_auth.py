from fastapi import Request, HTTPException
from pydantic import SecretStr
import jwt

from openhands.server import shared
from openhands.core.logger import openhands_logger as logger
from openhands.server.user_auth.user_auth import UserAuth
from openhands.storage.settings.file_settings_store import FileSettingsStore
from openhands.storage.secrets.file_secrets_store import FileSecretsStore
from openhands.server.settings import Settings
from openhands.storage.data_models.user_secrets import UserSecrets
from openhands.storage.secrets.secrets_store import SecretsStore
from openhands.storage.settings.settings_store import SettingsStore


class JwtUserAuth(UserAuth):

    _settings: Settings | None = None
    _settings_store: SettingsStore | None = None
    _secrets_store: SecretsStore | None = None
    _user_secrets: UserSecrets | None = None

    def __init__(self, user_id: str, token: str, email: str = None):
        self.user_id = user_id
        self.token = token
        self.email = email
        self._settings = None

    async def get_user_id(self) -> str | None:
        logger.info(f"get_user_id(): {self.user_id}")
        return self.user_id

    async def get_user_email(self) -> str | None:
        return self.email

    async def get_access_token(self) -> SecretStr | None:
        logger.info(f"get_access_token(): {SecretStr(self.token)}")
        return SecretStr(self.token)

    async def get_provider_tokens(self):
        logger.info(f"get_provider_tokens(): None")
        return None

    async def get_user_settings_store(self):
        logger.info(f"get_user_settings_store():  entry")
        # return FileSettingsStore(self.user_id)
        settings_store = self._settings_store
        if settings_store:
            return settings_store
        user_id = await self.get_user_id()
        settings_store = await shared.SettingsStoreImpl.get_instance(
            shared.config, user_id
        )
        if settings_store is None:
            raise ValueError('Failed to get settings store instance')
        self._settings_store = settings_store
        logger.info(f"get_user_settings_store():  exit")
        return settings_store

    async def get_user_settings(self) -> Settings | None:
        logger.info(f"get_user_settings():  entry")
        settings = self._settings
        if settings:
            return settings
        settings_store = await self.get_user_settings_store()
        settings = await settings_store.load()

        # Merge config.toml settings with stored settings
        if settings:
            settings = settings.merge_with_config_settings()

        self._settings = settings
        logger.info(f"get_user_settings():  exit")
        return settings

    async def get_secrets_store(self):
        # logger.info(f"get_secrets_store(): FileSecretsStore(self.user_id)")
        # return FileSecretsStore(self.user_id)
        logger.info(f"get_secrets_store(): entry")
        secrets_store = self._secrets_store
        if secrets_store:
            return secrets_store
        user_id = await self.get_user_id()
        secret_store = await shared.SecretsStoreImpl.get_instance(
            shared.config, user_id
        )
        if secret_store is None:
            raise ValueError('Failed to get secrets store instance')
        self._secrets_store = secret_store
        logger.info(f"get_secrets_store(): exit")
        return secret_store

    async def get_user_secrets(self) -> UserSecrets | None:
        logger.info(f"get_user_secrets(): entry")
        user_secrets = self._user_secrets
        if user_secrets:
            return user_secrets
        secrets_store = await self.get_secrets_store()
        user_secrets = await secrets_store.load()
        self._user_secrets = user_secrets
        logger.info(f"get_user_secrets(): exit")
        return user_secrets

    # async def get_user_secrets(self):
    #     logger.info("get_user_secrets(): await secrets_store.load()")
    #     secrets_store = await self.get_secrets_store()
    #     return await secrets_store.load()

    @classmethod
    async def get_for_user(cls, user_id: str) -> UserAuth:
        """Create a UserAuth instance for a specific user ID.
        This method is used when you need to create an auth instance
        without an HTTP request context.
        """
        # 对于 JWT 认证,这个方法可能不太适用
        # 因为通常需要从请求中获取 token
        # 但为了满足抽象类要求,可以这样实现:
        logger.info("get_for_user(): cls(user_id=user_id, token='', email=None)")
        return cls(user_id=user_id, token='', email=None)

    @classmethod
    async def get_instance(cls, request: Request) -> UserAuth:
        # logger.info(f"DEBUG: Full URL = {request.url}")
        # logger.info(f"DEBUG: All query_params = {dict(request.query_params)}")
        # logger.info(f"DEBUG: token = {request.query_params.get('token')}")
        # logger.info(f"DEBUG: Headers = {dict(request.headers)}")

        """支持三种方式提取 token:
        1. Authorization: Bearer header (推荐,用于后续请求)
        2. X-Session-API-Key header (用于 WebSocket)
        3. Query parameter ?token=xxx (仅用于初始登录)
        """
        token = None

        # 优先级 1: Authorization Bearer header
        auth_header = request.headers.get('Authorization') or request.headers.get('authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header[7:]
            if token:
                logger.info(f"{request.url}: using Authorization Bearer header")

        # 优先级 2: X-Session-API-Key header (用于 WebSocket)
        if not token:
            token = request.headers.get('X-Session-API-Key')
            if token:
                logger.info(f"{request.url}: using X-Session-API-Key header, for WebSocket")

        # 优先级 3: Query parameter (仅用于初始登录)
        if not token:
            token = request.query_params.get('token')
            if token:
                logger.info(f"{request.url}: using Query Parameter for token")

        if not token:
            logger.info(f"{request.url}: NOT FOUND TOKEN!!!")
            raise HTTPException(status_code=401, detail='No authentication token provided')

        # 验证 JWT token
        try:
            # from openhands.server.shared import server_config
            # jwt_secret = server_config.jwt_secret.get_secret_value()
            from openhands.server.shared import config
            jwt_secret = config.jwt_secret.get_secret_value()

            decoded = jwt.decode(token, jwt_secret, algorithms=['HS256'])

            user_id = decoded.get('user_id')
            email = decoded.get('email')

            if not user_id:
                logger.info(f"{request.url}: NOT FOUND user_id!!!")
                raise HTTPException(status_code=401, detail='Invalid token: missing user_id')

            logger.info(f"{request.url}: create JwtUserAuth.")
            return cls(user_id=user_id, token=token, email=email)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
