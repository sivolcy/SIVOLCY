from socketio.exceptions import ConnectionRefusedError

from openhands.core.config import load_openhands_config
from openhands.core.logger import openhands_logger as logger
from openhands.server.shared import ConversationStoreImpl
from openhands.storage.conversation.conversation_validator import ConversationValidator
import jwt


class CompareConversationValidator(ConversationValidator):
    """自定义对话验证器,使用 JWT token 进行身份验证"""

    async def _validate_conversation_access(
        self, conversation_id: str, user_id: str
    ) -> bool:
        """
        验证用户是否有权访问该对话

        Args:
            conversation_id: 对话 ID
            user_id: 用户 ID

        Returns:
            True 如果用户有权访问

        Raises:
            ConnectionRefusedError: 如果用户无权访问
        """
        config = load_openhands_config()
        conversation_store = await ConversationStoreImpl.get_instance(config, user_id)

        if not await conversation_store.validate_metadata(conversation_id, user_id):
            logger.error(
                f'User {user_id} is not allowed to join conversation {conversation_id}'
            )
            raise ConnectionRefusedError(
                f'User {user_id} is not allowed to join conversation {conversation_id}'
            )
        return True

    async def validate(
        self,
        conversation_id: str,
        cookies_str: str,
        authorization_header: str | None = None,
    ) -> str | None:
        """
        使用 JWT token 验证对话访问权限

        Args:
            conversation_id: 对话 ID
            cookies_str: Cookie 字符串(未使用)
            authorization_header: Authorization 请求头

        Returns:
            用户 ID 如果验证成功

        Raises:
            ConnectionRefusedError: 如果验证失败
        """
        # 检查 Authorization header
        if not authorization_header or not authorization_header.startswith('Bearer '):
            logger.warning('No valid Authorization header provided')
            raise ConnectionRefusedError('No valid Authorization header provided')

        # 提取 JWT token
        api_key = authorization_header.replace('Bearer ', '')

        # 验证 JWT token
        try:
            from openhands.server.shared import config

            if not config.jwt_secret:
                logger.error('JWT secret not configured')
                raise RuntimeError('JWT secret not found')

            jwt_secret = config.jwt_secret.get_secret_value()

            # 解码 JWT
            decoded = jwt.decode(api_key, jwt_secret, algorithms=['HS256'])

            user_id = decoded.get('user_id')
            email = decoded.get('email')

            if not user_id:
                logger.warning('JWT token missing user_id field')
                raise ConnectionRefusedError('Invalid token: missing user_id')

            logger.info(
                f'User {user_id} (email: {email}) is connecting to conversation {conversation_id} via JWT'
            )

            # 验证对话访问权限
            await self._validate_conversation_access(conversation_id, user_id)

            return user_id

        except jwt.ExpiredSignatureError:
            logger.warning('JWT token has expired')
            raise ConnectionRefusedError('Token has expired')
        except jwt.InvalidTokenError as e:
            logger.warning(f'Invalid JWT token: {e}')
            raise ConnectionRefusedError('Invalid token')
        except Exception as e:
            logger.error(f'Error validating JWT token: {e}')
            raise ConnectionRefusedError(f'Failed to validate token: {str(e)}')
