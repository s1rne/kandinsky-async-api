class ApiUrls:
    url_base = "https://api-key.fusionbrain.ai/key/api/v1/"

    url_text2image_run = f"{url_base}text2image/run"
    url_text2_image_status = f"{url_base}text2image/status/$uuid"


class WebUrls:
    url_base = "https://api.fusionbrain.ai/"
    url_base_login = "https://fusionbrain.ai/api/auth/"

    url_web = f"{url_base}web/api/v1/"

    url_csrf = f"{url_base_login}csrf/"
    url_keycloak = f"{url_base_login}signin/keycloak/"
    url_session = f"{url_base_login}session/"

    url_check_token = f"{url_web}text2image/availability?model_id=1"

    url_text2image_run = f"{url_web}text2image/run"
    url_text2_image_status = f"{url_web}text2image/status/$uuid"
