class BaseUrls:
    url_get_styles_base = "https://cdn.fusionbrain.ai/static/styles"
    url_api_base = "https://api-key.fusionbrain.ai/key/api/v1"
    url_web_base = "https://api.fusionbrain.ai/web/api/v1"
    url_login_base = "https://fusionbrain.ai/api/auth"

class ApiUrls:
    url_get_styles = f"{BaseUrls.url_get_styles_base}/key"

    url_pipelines = f"{BaseUrls.url_api_base}/pipelines"

    url_text2image_run = f"{BaseUrls.url_api_base}/pipeline/run"
    url_text2image_status = f"{BaseUrls.url_api_base}/pipeline/status/$uuid"

class WebUrls:
    url_csrf = f"{BaseUrls.url_login_base}/csrf/"
    url_keycloak = f"{BaseUrls.url_login_base}/signin/keycloak/"
    url_session = f"{BaseUrls.url_login_base}/session/"
    url_check_token = f"{BaseUrls.url_web_base}/text2image/availability"

    url_get_styles = f"{BaseUrls.url_get_styles_base}/web"

    url_pipelines = f"{BaseUrls.url_web_base}/pipelines"

    url_text2image_run = f"{BaseUrls.url_web_base}/text2image/run"
    url_text2image_status = f"{BaseUrls.url_web_base}/text2image/status/$uuid"

    url_text2animation_run = f"{BaseUrls.url_web_base}/animation/run"
    url_text2animation_status = f"{BaseUrls.url_web_base}/animation/status/$uuid"

    url_text2video_run = f"{BaseUrls.url_web_base}/text2video/run"
    url_text2video_status = f"{BaseUrls.url_web_base}/text2video/status/$uuid"