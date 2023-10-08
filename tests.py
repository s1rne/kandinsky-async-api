import asyncio

from PIL import Image

from api import FusionBrainApi

model = FusionBrainApi()


async def generate():
    img_bytes = await model.text2image("котик", style="CYBERPUNK")
    img = Image.open(img_bytes)
    img.save('cat_cyberpunk.jpg')


async def read_styles():
    for style in model.styles:
        print(style)
        print("\n")


if __name__ == '__main__':
    asyncio.run(read_styles())
    asyncio.run(generate())
