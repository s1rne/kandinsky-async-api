from __future__ import annotations

import asyncio
import base64
import json
import time
from io import BytesIO

import aiohttp

from .API_types import ApiApi, ApiWeb


class FusionBrainApi:
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
            n_url = self.api.urls.url_get_styles
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
            num_images: int | None = None,

            pipeline_id: int = 0, # currently: 0 == "Kandinsky 3.1", 1 == "Kandinsky 3.0", 2 == "Kandinsky 3.2"
            max_time: int = 2 * 60,  # max time generation on seconds (after return error)
            sleep_sec: int = 4
    ) -> BytesIO:
        params = await self.api.text2image_default_params.comb(
            style, width, height, art_gpt, prompt, negative_prompt, num_images
        )

        data = aiohttp.FormData()
        data.add_field("params",
                       json.dumps(params[0]),
                       content_type="application/json",
                       )

        async with aiohttp.ClientSession(headers=await self.api.get_headers()) as session:
            pipelines_url = self.api.urls.url_pipelines
            async with session.get(f"{pipelines_url}?type=TEXT2IMAGE") as resp:
                pipelines = await resp.json()

            n_url = self.api.urls.url_text2image_run
            if self.api.type == ApiApi.type:
                data.add_field(
                    "pipeline_id",
                    pipelines[pipeline_id]['id'],
                )
                async with session.post(f"{n_url}", data=data) as resp:
                    result = await resp.json()
            else:
                async with session.post(f"{n_url}?pipeline_id={pipelines[pipeline_id]['id']}", data=data) as resp:
                    result = await resp.json()
        if "error" in result:
            raise ValueError(result)

        uuid = result["uuid"]
        first_sleep_sec = result["status_time"] if "status_time" in result else 4
        return await self.polling(uuid, max_time, "img", sleep_sec, first_sleep_sec)

    async def text2animation(
            self,
            prompts: list[str],
            negative_prompts: list[str] | None = None,
            directions: list[str] | None = None,
            width: int | None = None,
            height: int | None = None,

            max_time: int = 5 * 60,  # max time generation on seconds (after return error)
            sleep_sec: int = 4
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

        async with aiohttp.ClientSession(headers=await self.api.get_headers()) as session:
            pipelines_url = self.api.urls.url_pipelines
            async with session.get(f"{pipelines_url}?type=ANIMATION") as resp:
                pipelines = await resp.json()

            n_url = self.api.urls.url_text2animation_run
            async with session.post(f"{n_url}?pipeline_id={pipelines[0]['id']}", data=data) as resp:
                result = await resp.json()

        if "error" in result:
            raise ValueError(result)

        uuid = result["uuid"]
        first_sleep_sec = result["status_time"] if "status_time" in result else 4
        return await self.polling(uuid, max_time, "anim", sleep_sec, first_sleep_sec)

    async def text2video(
            self,
            prompt: str,
            width: int | None = None,
            height: int | None = None,

            max_time: int = 6 * 60,  # max time generation on seconds (after return error)
            sleep_sec: int = 4
    ) -> BytesIO:
        if self.api.type != ApiWeb.type:
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

        async with aiohttp.ClientSession(headers=await self.api.get_headers()) as session:
            pipelines_url = self.api.urls.url_pipelines
            async with session.get(f"{pipelines_url}?type=TEXT2VIDEO") as resp:
                pipelines = await resp.json()

            n_url = self.api.urls.url_text2video_run
            async with session.post(f"{n_url}?pipeline_id={pipelines[0]['id']}", data=data) as resp:
                result = await resp.json()

        if "error" in result:
            raise ValueError(result)

        uuid = result["uuid"]
        first_sleep_sec = result["status_time"] if "status_time" in result else 4
        return await self.polling(uuid, max_time, "video", sleep_sec, first_sleep_sec)

    async def polling(self, uuid: str, max_time: int, type_generation: str, sleep_sec = 4, first_sleep_sec = 4) -> BytesIO:
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
                    censored = result["result"]["censored"] if self.api.type == ApiApi.type else result["censored"]
                    if isinstance(censored, bool) and censored or isinstance(censored, list) and any(censored):
                        raise ValueError("censored: is True")
                    else:
                        if type_generation == "img":
                            if self.api.type == ApiApi.type:
                                return BytesIO(base64.b64decode(result["result"]["files"][0]))
                            else:
                                async with session.get(result["images"][0]) as resp_img:
                                    if resp_img.status == 200:
                                        return BytesIO(await resp_img.read())
                                    else:
                                        raise ValueError("Fail install image from url")
                        elif type_generation in ["anim", "video"]:
                            return BytesIO(base64.b64decode(result["video"]))
                        else:
                            raise TypeError("type_generation must be 'img' or 'anim' or 'video'")
                elif result["status"] == "FAIL":
                    raise ValueError(f"status is FAIL: {result['status']}")

            await asyncio.sleep(sleep_sec)

        raise ValueError(f"timeout: {max_time} seconds")
