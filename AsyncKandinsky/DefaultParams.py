class Text2ImageDefaultParams:
    style = "DEFAULT"
    width = 1024
    height = 1024
    art_gpt = False
    prompt = "Cat"
    negative_prompt = ""
    num_images = 1

    async def comb(
            self,
            style: str,
            width: int,
            height: int,
            art_gpt: bool,
            prompt: str,
            negative_prompt: str,
            num_images: str
    ) -> list:
        _style = style or self.style
        _width = width or self.width
        _height = height or self.height
        _art_gpt = art_gpt or self.art_gpt
        _prompt = prompt or self.prompt
        _negative_prompt = negative_prompt or self.negative_prompt
        _num_images = num_images or self.num_images

        return [
            {
                "type": "GENERATE",
                "style": _style,
                "width": _width,
                "height": _height,
                "numImages": _num_images,
                "censor": {"useGigaBeautificator": art_gpt},
                "generateParams": {"query": _prompt},
                "negativePromptDecoder": _negative_prompt
            }
        ]


class Text2AnimationDefaultParams:
    prompts = ["Cat", "Cat"]
    negative_prompts = ["", ""]
    directions = ["LEFT_SINUS_Y", "LEFT_SINUS_Y"]
    width = 640
    height = 640

    async def comb(
            self,
            prompts: list[str],
            negative_prompts: list[str],
            directions: list[str],
            width: int,
            height: int
    ) -> list:
        _width = self.width if width is None else width
        _height = self.height if height is None else height
        _directions = self.directions if directions is None else directions
        _prompts = self.prompts if prompts is None else prompts
        _negative_prompts = self.negative_prompts if negative_prompts is None else negative_prompts

        return [
            {
                "width": _width,
                "height": _height,
                "animation_steps": [
                    {
                        "prompt": _prompts[x],
                        "negative_prompt": _negative_prompts[x],
                        "direction": _directions[x],
                        "acceleration": "1"
                    }
                    for x in range(2)
                ]
            }
        ]


class Text2VideoDefaultParams:
    prompt = "Cat"
    width = 512
    height = 512

    async def comb(
            self,
            prompt: str,
            width: int,
            height: int
    ) -> list:
        _width = self.width if width is None else width
        _height = self.height if height is None else height
        _prompt = self.prompt if prompt is None else prompt

        return [
            {
                "width": _width,
                "height": _height,
                "prompt": _prompt
            }
        ]
