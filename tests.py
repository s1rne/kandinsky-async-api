import asyncio

from PIL import Image

from api import FusionBrainApi

model = FusionBrainApi("Сюда свой api_key", "Сюда свой secret_key")


async def generate():
    img_bytes = await model.text2image("котик", style="ANIME")
    img = Image.open(img_bytes)
    img.save('cat_anime.jpg')


async def read_styles():
    for style in await model.get_styles():
        print(style)
        print("\n")


if __name__ == '__main__':
    asyncio.run(read_styles())
    asyncio.run(generate())
