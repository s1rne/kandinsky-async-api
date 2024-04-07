class ApiApi:
    type = "api"

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key


class ApiWeb:
    type = "web"

    def __init__(self, authorization: str):
        self.authorization = authorization if authorization.startswith("Bearer ") else f"Bearer {authorization}"
