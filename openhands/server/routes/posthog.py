from fastapi import FastAPI
def add_posthog_endpoints(app: FastAPI):
    @app.api_route('/api/posthog/e/', methods=['GET','POST'])
    async def posthog_event():
        return 'OK'

    @app.api_route('/api/posthog/flags/', methods=['GET','POST'])
    async def posthog_flags():
        return 'OK'

    @app.get("/api/posthog/array/{phc_id}/config.js")
    async def handle_config_js_request(phc_id: str):
        """
        匹配 /api/posthog/array/{phc_id}/config.js 格式的 URL，
        其中 {phc_id} 是动态的，但我们不关心其具体值。
        """
        # 这里的 phc_id 变量会接收到动态匹配到的值，但我们在此处不使用它
        return {}

    @app.get("/api/posthog/array/{phc_id}/config")
    async def handle_config_request(phc_id: str):
        """
        匹配 /api/posthog/array/{phc_id}/config 格式的 URL，
        其中 {phc_id} 是动态的，但我们不关心其具体值。
        """
        # 这里的 phc_id 变量会接收到动态匹配到的值，但我们在此处不使用它
        return "OK"

    @app.api_route("/api/posthog/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def posthog_catch_all(path: str):
        return "OK from catch-all"
