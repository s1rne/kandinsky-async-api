import re

import aiohttp

from .URLS import WebUrls, ApiUrls


class ApiApi:
    type = "api"

    model_numbers = {
        "3.0": "4"
    }
    urls = ApiUrls

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key

    async def get_headers(self) -> dict:
        return {"X-Key": f"Key {self.api_key}", "X-Secret": f"Secret {self.secret_key}"}


class ApiWeb:
    type = "web"

    model_numbers = {
        "3.0": "1"
    }
    urls = WebUrls

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

        self.accessToken = ""
        self.refreshToken = ""

    async def update_tokens(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(WebUrls.url_csrf) as response:
                csrf_token = await response.json()

            async with session.post(WebUrls.url_keycloak, data={
                "csrfToken": csrf_token["csrfToken"],
                "json": "true"
            }) as response:
                new_url = (await response.json())["url"]

            async with session.get(new_url) as response:
                new_url = re.findall(r'action=[\'"]?([^\'" >]+)', await response.text())[0].replace("amp;", "")

            await session.post(new_url, data={"username": self.email, "password": self.password, "credentialId": ""})

            async with session.get(WebUrls.url_session) as response:
                user_data = await response.json()
                self.accessToken = user_data["accessToken"]
                self.refreshToken = user_data["refreshToken"]

    async def check_accessToken(self):
        if self.accessToken == "":
            await self.update_tokens()
        async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {self.accessToken}"}) as session:
            async with session.get(WebUrls.url_check_token) as response:
                if response.status != 200:
                    await self.update_tokens()

    async def get_headers(self) -> dict:
        await self.check_accessToken()

        return {"Authorization": f"Bearer {self.accessToken}"}
