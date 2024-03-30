import asyncio
import base64
import json
import time
from io import BytesIO

import aiohttp


class FusionBrainApi:
    url_get_styles = "https://cdn.fusionbrain.ai/static/styles/api"

    url_text2image_run = "https://api-key.fusionbrain.ai/key/api/v1/text2image/run"
    url_text2_image_status = "https://api-key.fusionbrain.ai/key/api/v1/text2image/status/$uuid"

    def __init__(self, api_key: str, secret_key: str):
        self.api_headers = {
            "X-Key": f"Key {api_key}",
            "X-Secret": f"Secret {secret_key}",
        }

    async def get_styles(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url_get_styles, ssl=False) as response:
                return await response.json()

    async def text2image(self,
                         prompt: str = "",
                         negative_prompt: str = "",
                         style: str = "DEFAULT",
                         width: int = 1024,
                         height: int = 1024,

                         max_time: int = 120  # max time generation on seconds (after return error)
                         ) -> dict:

        params = {
            "type": "GENERATE",
            "style": style,
            "width": width,
            "height": height,
            "generateParams": {"query": prompt},
            "negativePromptDecoder": negative_prompt
        }

        data = aiohttp.FormData()
        data.add_field("params",
                       json.dumps(params),
                       content_type="application/json")
        data.add_field("model_id", "4")

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url_text2image_run, data=data, headers=self.api_headers, ssl=False) as resp:
                result = await resp.json()

        if "error" in result:
            return {"error": True, "data": result}

        uuid = result["uuid"]
        start_time = time.time()
        while time.time() - (start_time + max_time) < 0:
            async with aiohttp.ClientSession() as session:
                _url = self.url_text2_image_status.replace("$uuid", uuid)
                async with session.get(_url, headers=self.api_headers, ssl=False) as resp:
                    result = await resp.json()
                    if result["status"] == "DONE":
                        return {"error": False, "data": BytesIO(base64.b64decode(result["images"][0]))}

            await asyncio.sleep(4)

        return {"error": True, "data": f"timeout: {max_time} seconds"}
