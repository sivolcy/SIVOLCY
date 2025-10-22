from openhands.server.config.server_config import ServerConfig

class CustomServerConfig(ServerConfig):
    user_auth_class: str = 'comparegpt.server.auth.jwt_user_auth.JwtUserAuth'
