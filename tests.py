import asyncio

from PIL import Image

from AsyncKandinsky import FusionBrainApi, ApiApi, ApiWeb

model = FusionBrainApi(ApiApi("Сюда свой api_key", "Сюда свой secret_key"))
# Любой способ на выбор
model = FusionBrainApi(ApiWeb("Ваша почта", "Ваш пароль"))


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


if __name__ == '__main__':
    asyncio.run(read_styles())
    asyncio.run(generate())
