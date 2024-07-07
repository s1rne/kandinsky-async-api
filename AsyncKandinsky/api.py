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

    async def text2image(
            self,
            prompt: str,
            negative_prompt: str | None = None,
            style: str | None = None,
            width: int | None = None,
            height: int | None = None,
            art_gpt: bool | None = None,
            model: str | None = None,  # don`t touch (only 3.1)

            max_time: int = 2 * 60  # max time generation on seconds (after return error)
    ) -> BytesIO:
        params, model = await self.api.text2image_default_params.comb(
            style, width, height, art_gpt, model, prompt, negative_prompt
        )

        data = aiohttp.FormData()
        data.add_field("params",
                       json.dumps(params),
                       content_type="application/json",
                       )
        data.add_field("model_id", "1" if self.api.type == "web" else "4")

        async with aiohttp.ClientSession(headers=await self.api.get_headers()) as session:
            n_url = self.api.urls.url_text2image_run
            async with session.post(n_url, data=data) as resp:
                result = await resp.json()

        if "error" in result:
            raise ValueError(result)

        uuid = result["uuid"]
        return await self.polling(uuid, max_time, "img")

    async def text2animation(
            self,
            prompts: list[str],
            negative_prompts: list[str] | None = None,
            directions: list[str] | None = None,
            width: int | None = None,
            height: int | None = None,

            max_time: int = 5 * 60  # max time generation on seconds (after return error)
    ) -> BytesIO:
        if self.api.type != "web":
            raise TypeError("text2animation only supports web")

        params = await self.api.text2animation_default_params.comb(
            prompts, negative_prompts, directions, width, height
        )
        params = params[0]

        data = aiohttp.FormData()
        data.add_field("params",
                       json.dumps(params),
                       content_type="application/json",
                       )
        data.add_field("model_id", "2")

        async with aiohttp.ClientSession(headers=await self.api.get_headers()) as session:
            n_url = self.api.urls.url_text2animation_run
            async with session.post(n_url, data=data) as resp:
                result = await resp.json()

        if "error" in result:
            raise ValueError(result)

        uuid = result["uuid"]
        return await self.polling(uuid, max_time, "anim")

    async def text2video(
            self,
            prompt: str,
            width: int | None = None,
            height: int | None = None,

            max_time: int = 6 * 60  # max time generation on seconds (after return error)
    ) -> BytesIO:
        if self.api.type != "web":
            raise TypeError("text2video only supports web")

        params = await self.api.text2video_default_params.comb(
            prompt, width, height
        )
        params = params[0]

        data = aiohttp.FormData()
        data.add_field("params",
                       json.dumps(params),
                       content_type="application/json",
                       )
        data.add_field("model_id", "3")

        async with aiohttp.ClientSession(headers=await self.api.get_headers()) as session:
            n_url = self.api.urls.url_text2video_run
            async with session.post(n_url, data=data) as resp:
                result = await resp.json()

        if "error" in result:
            raise ValueError(result)

        uuid = result["uuid"]
        return await self.polling(uuid, max_time, "video")

    async def polling(self, uuid: str, max_time: int, type_generation: str) -> BytesIO:
        start_time = time.time()
        while time.time() - (start_time + max_time) < 0:
            async with aiohttp.ClientSession(headers=await self.api.get_headers()) as session:
                if type_generation == "img":
                    n_url = self.api.urls.url_text2image_status
                elif type_generation == "anim":
                    n_url = self.api.urls.url_text2animation_status
                elif type_generation == "video":
                    n_url = self.api.urls.url_text2video_status
                else:
                    raise TypeError("type_generation must be 'img' or 'anim' or 'video'")
                n_url = n_url.replace("$uuid", uuid)
                async with session.get(n_url) as resp:
                    result = await resp.json()
                    if result["status"] == "DONE":
                        censored = result["censored"]
                        if isinstance(censored, bool) and censored or isinstance(censored, list) and any(censored):
                            raise ValueError("censored: is True")
                        else:
                            if type_generation == "img":
                                async with session.get(result["images"][0]) as resp_img:
                                    if resp_img.status == 200:
                                        # return {"error": False, "data": BytesIO(await resp_img.read())}
                                        return BytesIO(await resp_img.read())
                                    else:
                                        # return {"error": True, "data": "Fail install image from url"}
                                        raise ValueError("Fail install image from url")
                            elif type_generation in ["anim", "video"]:
                                return BytesIO(base64.b64decode(result["video"]))
                            else:
                                raise TypeError("type_generation must be 'img' or 'anim' or 'video'")
                    elif result["status"] == "FAIL":
                        raise ValueError(f"status is FAIL: {result['status']}")

            await asyncio.sleep(4)

        raise ValueError(f"timeout: {max_time} seconds")
