from __future__ import annotations

import asyncio
import base64
import json
import time
from io import BytesIO

import aiohttp

from .API_types import ApiApi, ApiWeb


class FusionBrainApi:
    url_get_styles = "https://cdn.fusionbrain.ai/static/styles/$api_type"

    def __init__(self, api: ApiApi | ApiWeb):
        if hasattr(api, "type"):
            if api.type not in [ApiApi.type, ApiWeb.type]:
                raise TypeError("Invalid API type")
            else:
                self.api = api
        else:
            raise TypeError("Invalid API structure")

    async def get_styles(self) -> dict:
        async with aiohttp.ClientSession() as session:
            n_url = self.url_get_styles.replace("$api_type", self.api.type)
            async with session.get(n_url) as response:
                return await response.json()

    async def text2image(self,
                         prompt: str = "",
                         negative_prompt: str = "",
                         style: str = "DEFAULT",
                         width: int = 1024,
                         height: int = 1024,
                         model: str = "3.0",  # don`t touch (only 3.0)

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
                       content_type="application/json",
                       )
        data.add_field("model_id", self.api.model_numbers[model])

        async with aiohttp.ClientSession() as session:
            n_url = self.api.urls.url_text2image_run
            async with session.post(n_url, data=data, headers=await self.api.get_headers()) as resp:
                result = await resp.json()

        if "error" in result:
            return {"error": True, "data": result}

        uuid = result["uuid"]
        start_time = time.time()
        while time.time() - (start_time + max_time) < 0:
            async with aiohttp.ClientSession() as session:
                n_url = self.api.urls.url_text2_image_status.replace("$uuid", uuid)
                async with session.get(n_url, headers=await self.api.get_headers()) as resp:
                    result = await resp.json()
                    if result["status"] == "DONE":
                        if result["censored"]:
                            return {"error": True, "data": "censored: is True"}
                        else:
                            return {"error": False, "data": BytesIO(base64.b64decode(result["images"][0]))}
                    elif result["status"] == "FAIL":
                        return {"error": True, "data": f"status is FAIL: {result['status']}"}

            await asyncio.sleep(4)

        return {"error": True, "data": f"timeout: {max_time} seconds"}
