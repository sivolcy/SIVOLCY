from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from openhands.server.user_auth import get_user_id   #, get_user_email

app = APIRouter(prefix='/api')

@app.get('/check_auth')
async def check_auth(request: Request):
    """
    验证 JWT token 是否有效

    从 Authorization header 或查询参数中提取 token,
    通过 JwtUserAuth 验证其有效性

    Returns:
        200: Token 有效,返回用户信息
        401: Token 无效或缺失
    """
    try:
        # 调用 get_user_id 会触发 JwtUserAuth.get_instance() 验证 token
        user_id = await get_user_id(request)
        # user_email = await get_user_email(request)

        if not user_id:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={'error': 'Invalid token: missing user_id'}
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'authenticated': True,
                'user_id': user_id,
                # 'email': user_email
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                'authenticated': False,
                'error': str(e)
            }
        )


