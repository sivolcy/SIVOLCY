import sys
import traceback

from fastapi import Request, status
from fastapi.responses import JSONResponse

from openhands.core.logger import openhands_logger as logger


class AuthMiddleware:
    async def __call__(self, request: Request, call_next):
        # 跳过健康检查和公开端点
        public_paths = [
            '/api/health',
            '/api/public',
            '/api/options/config',  # 前端需要在认证前获取配置
            '/assets/',  # 静态资源
            '/locales/',
            '/favicon.ico',
            '/mcp/mcp',
            # '/api/check_auth',
            # '/mcp/sse',
            # '/mcp',
        ]
        # 跳过公开端点
        if any(request.url.path.startswith(path) for path in public_paths):
            logger.debug(f'{request.url.path} is PUBLIC PATH, skip token checking ...')
            return await call_next(request)

        try:
            logger.debug(f'{request.url.path}: Before get_user_auth ...  ')
            # 这会触发 JwtUserAuth.get_instance(),验证 token
            from openhands.server.user_auth.user_auth import get_user_auth

            user_auth = await get_user_auth(request)
            logger.debug(
                f'{request.url.path}: After get_user_auth, user_id={await user_auth.get_user_id()}.  '
                f'request.state.user_auth set: {hasattr(request.state, "user_auth")}. '
            )

            logger.debug(f'{request.url.path}: Before call_next ... ')
            response = await call_next(request)
            logger.debug(
                f'{request.url.path}: After call_next, status={response.status_code}'
            )

            return response
        except Exception as e:
            logger.error(f'AuthMiddleware: Exception during authentication: {str(e)}')
            traceback.print_exc(file=sys.stdout)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, content={'error': str(e)}
            )
