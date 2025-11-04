from fastapi import Request, HTTPException
from pydantic import SecretStr
import jwt

from openhands.server import shared
from openhands.core.logger import openhands_logger as logger
from openhands.server.user_auth.user_auth import UserAuth, AuthType # 确保导入 AuthType
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

    def __init__(self, user_id: str,
                 token: str,
                 email: str,
                 user_name: str,
                 role: str,
                 api_key: str,
                 expiration: int,
                 ):
        self.user_id = user_id
        self.user_name = user_name
        self.role = role
        self.api_key = api_key
        self.expiration = expiration
        self.token = token
        self.email = email
        self._settings = None
        # ======================= MODIFICATION START =======================
        # 添加 auth_type 属性，以满足 manage_conversations.py 中的检查
        # 因为 JWT 认证是一种 Bearer token 认证，所以我们将其硬编码为 BEARER
        self.auth_type = AuthType.BEARER
        # ======================= MODIFICATION END =======================

    async def get_user_id(self) -> str | None:
        logger.debug(f"get_user_id(): {self.user_id}")
        return self.user_id

    async def get_user_email(self) -> str | None:
        return self.email

    async def get_access_token(self) -> SecretStr | None:
        logger.debug(f"get_access_token(): {SecretStr(self.token)}")
        return SecretStr(self.token)

    async def get_provider_tokens(self):
        logger.debug(f"get_provider_tokens(): entry")
        secrets_store = await self.get_secrets_store()
        user_secrets = await secrets_store.load()
        if user_secrets:
            return user_secrets.provider_tokens
        return None

    async def get_user_settings_store(self):
        logger.debug(f"get_user_settings_store(): entry")
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
        logger.debug(f"get_user_settings_store():  exit")
        return settings_store

    async def get_user_settings(self) -> Settings | None:
        logger.debug(f"get_user_settings():  entry")
        settings = self._settings
        if settings:
            return settings
        settings_store = await self.get_user_settings_store()
        settings = await settings_store.load()

        # 从 config.toml 获取默认配置
        config_settings = Settings.from_config()
        if not config_settings:
            logger.error(f"##### NOT FOUND config.toml! #####")
            raise Exception('NOT FOUND config.toml.')

        if not config_settings.llm_base_url or not config_settings.llm_model:
            logger.error(f"##### NOT FOUND base_url and model setting in config.toml! #####")
            raise Exception('NOT FOUND base_url and model setting in config.toml.')


        # logger.info(f"##### Updating Settings for user {self.user_id}  ...")

        # # 使用 config.toml 的值,但覆盖 API key 为 JWT 中的值
        # settings = Settings(
        #     llm_model=config_settings.llm_model,  # 从 config.toml 读取
        #     llm_api_key=SecretStr(self.api_key),  # 使用 JWT 中的 api_key
        #     llm_base_url=config_settings.llm_base_url,  # 从 config.toml 读取
        #     agent=config_settings.agent,
        #     max_iterations=config_settings.max_iterations,
        #     # security_analyzer=config_settings.security_analyzer,
        #     # confirmation_mode=config_settings.confirmation_mode,
        # )

        # # Merge config.toml settings with stored settings
        # if settings:
        #     settings = settings.merge_with_config_settings()

        # # 保存默认配置
        # await settings_store.store(settings)
        # logger.info(f"##### Saved Settings for user {self.user_id}.")

        # self._settings = settings
        # logger.debug(f"get_user_settings():  exit")
        # return settings


        # 如果没有存储的 settings,创建默认配置
        if not settings:
            logger.info(f"##### No existing settings for user {self.user_id}, creating defaults ...")

            # 使用 config.toml 的值,但覆盖 API key 为 JWT 中的值
            settings = Settings(
                llm_model=config_settings.llm_model,  # 从 config.toml 读取
                llm_api_key=SecretStr(self.api_key),  # 使用 JWT 中的 api_key
                llm_base_url=config_settings.llm_base_url,  # 从 config.toml 读取
                agent=config_settings.agent,
                max_iterations=config_settings.max_iterations,
                # security_analyzer=config_settings.security_analyzer,
                # confirmation_mode=config_settings.confirmation_mode,
            )

            # 保存默认配置
            await settings_store.store(settings)
            logger.info(f"##### Default settings saved for user {self.user_id}")
        else:
            # # 如果存在 settings 但缺少 LLM 配置,更新它们
            # if not settings.llm_api_key:
            #     settings.llm_api_key = SecretStr(self.api_key)
            # if not settings.llm_base_url:
            #     settings.llm_base_url = config_settings.llm_base_url

            # 如果传入的 api_key 有更新，与个人存储的不一致，或者系统配置的llm_base_url与 个人存储base_url 不同，则更新个人存储。
            if SecretStr(self.api_key) != settings.llm_api_key  or  config_settings.llm_base_url != settings.llm_base_url:
                logger.info(f"##### Found existing settings for user {self.user_id}, updating api_key and llm_base_url ...")
                logger.debug(f"####### NOT EQUAL ##########")

                # 更新 API key 为 JWT 中的值，更新 base_url
                settings = Settings(
                    llm_model=settings.llm_model,  # 保留原有个人的模型设置
                    llm_api_key=SecretStr(self.api_key),  # 更新为 JWT 中的 api_key
                    llm_base_url=config_settings.llm_base_url,  # 从 config.toml 读取
                    agent=config_settings.agent,
                    max_iterations=config_settings.max_iterations,
                    # security_analyzer=config_settings.security_analyzer,
                    # confirmation_mode=config_settings.confirmation_mode,
                )
            else:
                logger.debug(f"####### EQUAL ##########")

            await settings_store.store(settings)
            logger.info(f"##### Settings updated for user {self.user_id}")

        # Merge config.toml settings with stored settings
        if settings:
            settings = settings.merge_with_config_settings()

        self._settings = settings
        logger.debug(f"get_user_settings():  exit")
        return settings

    # async def get_user_settings(self) -> Settings:
    #     """
    #     加载用户设置，如果不存在则创建。
    #     """
    #     logger.debug("get_user_settings(): entry")
    #     if self._settings:
    #         return self._settings

    #     settings_store = await self.get_user_settings_store()
    #     settings = await settings_store.load()

    #     # 如果设置不存在，则创建默认设置
    #     if not settings:
    #         settings = await self._create_and_store_default_settings(settings_store)
    #     # 如果 JWT 中的 API Key 与存储的不一致，则更新
    #     elif settings.llm_api_key.get_secret_value() != self.api_key:
    #         settings = await self._update_settings_with_new_key(settings_store, settings)

    #     # 与全局配置合并
    #     settings = settings.merge_with_config_settings()

    #     self._settings = settings
    #     logger.debug("get_user_settings(): exit")
    #     return settings

    async def _create_and_store_default_settings(self, store: SettingsStore) -> Settings:
        """创建一个新的默认设置并保存。"""
        logger.info(f"No existing settings for user {self.user_id}, creating defaults...")
        config_settings = Settings.from_config()
        if not config_settings:
            raise HTTPException(status_code=500, detail="Server default configuration (config.toml) is missing or invalid.")

        new_settings = Settings(
            llm_model=config_settings.llm_model,
            llm_api_key=SecretStr(self.api_key), # 使用来自 JWT 的 key
            llm_base_url=config_settings.llm_base_url,
            agent=config_settings.agent,
            max_iterations=config_settings.max_iterations,
        )
        await store.store(new_settings)
        logger.info(f"Default settings saved for user {self.user_id}")
        return new_settings

    async def _update_settings_with_new_key(self, store: SettingsStore, existing_settings: Settings) -> Settings:
        """使用来自 JWT 的新 API Key 更新现有设置。"""
        logger.info(f"API key for user {self.user_id} has changed, updating stored settings.")
        config_settings = Settings.from_config()
        if not config_settings:
            raise HTTPException(status_code=500, detail="Server default configuration (config.toml) is missing or invalid.")

        existing_settings.llm_api_key = SecretStr(self.api_key)
        existing_settings.llm_base_url = config_settings.llm_base_url
        await store.store(existing_settings)
        logger.info(f"Settings updated with new API key for user {self.user_id}")
        return existing_settings


    async def get_secrets_store(self):
        # logger.info(f"get_secrets_store(): FileSecretsStore(self.user_id)")
        # return FileSecretsStore(self.user_id)
        logger.debug(f"get_secrets_store(): entry")
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
        logger.debug(f"get_secrets_store(): exit")
        return secret_store

    async def get_llm_credentials(self) -> dict[str, str]:
        """Expose provider/base_url/api_key parsed from JWT for downstream services."""
        if not self.api_key:
            raise HTTPException(status_code=401, detail='Missing LLM API key in token')  # 确保所有 LLM 调用都有凭证

        config_settings = Settings.from_config()

        # base_url = ""
        # if config_settings:
        #     base_url = config_settings.llm_base_url
        # else:
        #     base_url = 'https://comparegpt.io/api'

        base_url = (
            config_settings.llm_base_url
            if config_settings and config_settings.llm_base_url
            else 'https://comparegpt.io/api'
        )

        return {
            'provider': 'comparegpt',  # provider 固定
            'base_url': base_url,
            'api_key': self.api_key,  # 来自 JWT
            # 'api_key': "cgpt_oOtQljEyoYBHvW3F2MmZX218yROo3lrn"
        }

    async def get_user_secrets(self) -> UserSecrets | None:
        logger.debug(f"get_user_secrets(): entry")
        user_secrets = self._user_secrets
        if user_secrets:
            return user_secrets
        secrets_store = await self.get_secrets_store()
        user_secrets = await secrets_store.load()
        self._user_secrets = user_secrets
        logger.debug(f"get_user_secrets(): exit")
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
        logger.debug("get_for_user(): cls(user_id=user_id, token='', email=None)")
        return cls(user_id=user_id, token='', email='', user_name='', role='', api_key='', expiration=0)

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

            # 1. 安全地获取 jwt_secret 对象
            jwt_secret_obj = config.jwt_secret

            # 2. 检查对象是否存在，如果不存在则抛出异常
            if jwt_secret_obj is None:
                raise HTTPException(status_code=500, detail="JWT secret is not configured on the server.")

            # 3. 只有在检查通过后，才安全地调用 get_secret_value()
            jwt_secret = jwt_secret_obj.get_secret_value()

            decoded = jwt.decode(token, jwt_secret, algorithms=['HS256'])

            user_id = decoded.get('user_id')
            email = decoded.get('email')
            user_name = decoded.get('user_name')
            role = decoded.get('role')
            api_key = decoded.get('api_key')
            expiration_str = decoded.get('exp')
            expiration = int(expiration_str) if str(expiration_str).isdigit() else None

            if not user_id:
                logger.info(f"{request.url}: NOT FOUND user_id!!!")
                raise HTTPException(status_code=401, detail='Invalid token: missing user_id')

            if not api_key:
                logger.info(f"{request.url}: NOT FOUND api_key!!!")
                raise HTTPException(status_code=401, detail='Invalid token: missing api_key')

            if not expiration:
                logger.info(f"{request.url}: NOT FOUND expiration!!!")
                raise HTTPException(status_code=401, detail='Invalid token: missing expiration')

            logger.info(f"{request.url}: create JwtUserAuth.")
            return cls(user_id=user_id,
                       token=token,
                       email=email,
                       user_name=user_name,
                       role=role,
                       api_key=api_key,
                       expiration=expiration)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
