class Text2ImageDefaultParams:
    style = "DEFAULT"
    width = 1024
    height = 1024
    art_gpt = False
    model = "3.0"
    prompt = "Cat"
    negative_prompt = ""

    async def comb(
            self,
            style: str,
            width: int,
            height: int,
            art_gpt: bool,
            model: str,
            prompt: str,
            negative_prompt: str,
    ) -> list:
        _style = self.style if style is None else style
        _width = self.width if width is None else width
        _height = self.height if height is None else height
        _art_gpt = self.art_gpt if art_gpt is None else art_gpt
        _model = self.model
        _prompt = self.prompt if prompt is None else prompt
        _negative_prompt = self.negative_prompt if negative_prompt is None else negative_prompt

        return [
            {
                "type": "GENERATE",
                "style": _style,
                "width": _width,
                "height": _height,
                "censor": {"useGigaBeautificator": art_gpt},
                "generateParams": {"query": _prompt},
                "negativePromptDecoder": _negative_prompt
            },
            _model
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
