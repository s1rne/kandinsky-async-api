import asyncio

from PIL import Image

from AsyncKandinsky import FusionBrainApi, ApiApi

model = FusionBrainApi(ApiApi("Сюда свой api_key", "Сюда свой secret_key"))


async def generate():
    result = await model.text2image("котик", style="ANIME")
    if result["error"]:
        print("Error:")
        print(result["data"])
    else:
        img = Image.open(result["data"])
        img.save('cat_anime.jpg')
        print("Done!")


async def read_styles():
    for style in await model.get_styles():
        print(style)
        print("\n")


if __name__ == '__main__':
    asyncio.run(read_styles())
    asyncio.run(generate())
