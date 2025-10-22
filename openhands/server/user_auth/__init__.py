from fastapi import Request
from pydantic import SecretStr

from openhands.integrations.provider import PROVIDER_TOKEN_TYPE
from openhands.server.settings import Settings
from openhands.server.user_auth.user_auth import AuthType, get_user_auth
from openhands.storage.data_models.user_secrets import UserSecrets
from openhands.storage.secrets.secrets_store import SecretsStore
from openhands.storage.settings.settings_store import SettingsStore
from openhands.core.logger import openhands_logger as logger

async def get_provider_tokens(request: Request) -> PROVIDER_TOKEN_TYPE | None:
    logger.debug("get_provider_tokens() entry")
    user_auth = await get_user_auth(request)
    provider_tokens = await user_auth.get_provider_tokens()
    logger.debug("get_provider_tokens() exit")
    return provider_tokens


async def get_access_token(request: Request) -> SecretStr | None:
    logger.debug("get_access_token() entry")
    user_auth = await get_user_auth(request)
    access_token = await user_auth.get_access_token()
    logger.debug("get_access_token() exit")
    return access_token


async def get_user_id(request: Request) -> str | None:
    logger.debug("get_user_id() entry")
    user_auth = await get_user_auth(request)
    user_id = await user_auth.get_user_id()
    logger.debug("get_user_id() exit")
    return user_id


async def get_user_settings(request: Request) -> Settings | None:
    logger.debug("get_user_settings() entry")
    user_auth = await get_user_auth(request)
    logger.debug("get_user_settings() 01 - get_user_settings() ")
    user_settings = await user_auth.get_user_settings()
    logger.debug("get_user_settings() exit")
    return user_settings


async def get_secrets_store(request: Request) -> SecretsStore:
    logger.debug("get_secrets_store() entry")
    user_auth = await get_user_auth(request)
    secrets_store = await user_auth.get_secrets_store()
    logger.debug("get_secrets_store() exit")
    return secrets_store


async def get_user_secrets(request: Request) -> UserSecrets | None:
    logger.debug("get_user_secrets() entry")
    user_auth = await get_user_auth(request)
    user_secrets = await user_auth.get_user_secrets()
    logger.debug("get_user_secrets() exit")
    return user_secrets


async def get_user_settings_store(request: Request) -> SettingsStore | None:
    logger.debug("get_user_settings_store() entry")
    user_auth = await get_user_auth(request)
    user_settings_store = await user_auth.get_user_settings_store()
    logger.debug("get_user_settings_store() exit")
    return user_settings_store


async def get_auth_type(request: Request) -> AuthType | None:
    logger.debug("get_auth_type() entry")
    user_auth = await get_user_auth(request)
    logger.debug("get_auth_type() exit")
    return user_auth.get_auth_type()
