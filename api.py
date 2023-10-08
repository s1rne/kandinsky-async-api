import asyncio
import base64
import json
from io import BytesIO

import aiohttp


class FusionBrainApi:
    url_get_styles = "https://cdn.fusionbrain.ai/static/styles/web"
    url_text2image_run = "https://api.fusionbrain.ai/web/api/v1/text2image/run"
    url_text2_image_status = "https://api.fusionbrain.ai/web/api/v1/text2image/status/$uuid"

    styles = [""]

    def __init__(self):
        asyncio.run(self.load_styles())

    async def load_styles(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url_get_styles) as response:
                self.styles = await response.json()

    async def text2image(self,
                         prompt: str = "",
                         negative_prompt: str = "",
                         style: str = "DEFAULT",
                         width: int = 1024,
                         height: int = 1024
                         ) -> BytesIO:

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
        data.add_field("model_id", "1")

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url_text2image_run, data=data) as response:
                result = await response.json()
        if "error" in result:
            return result

        uuid = result["uuid"]
        for attempt in range(20):
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url_text2_image_status.replace("$uuid", uuid)) as response:
                    result = await response.json()
                    if result["status"] == "DONE":
                        break
                    print(result)

            await asyncio.sleep(1)
        img_bytes = base64.b64decode(result["images"][0])
        return BytesIO(img_bytes)
