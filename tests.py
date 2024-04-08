import asyncio

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
        with open("cat_anime_img.png", "wb") as f:
            f.write(result["data"].getvalue())
        print("Done!")

    # _______________________________________________________________________________________

    result = await model.text2video("котик бежит по полю")
    # Стиль придётся самому вписывать
    if result["error"]:
        print("Error:")
        print(result["data"])
    else:
        with open("cat_anime_video.mp4", "wb") as f:
            f.write(result["data"].getvalue())
        print("Done!")

    # _______________________________________________________________________________________

    result = await model.text2animation(["котик бежит по полю", "котик пьёт воду из речки"])
    # Стиль придётся самому вписывать
    if result["error"]:
        print("Error:")
        print(result["data"])
    else:
        with open("cat_anime_animation.mp4", "wb") as f:
            f.write(result["data"].getvalue())
        print("Done!")


async def read_styles():
    for style in await model.get_styles():
        print(style)


if __name__ == '__main__':
    asyncio.run(read_styles())
    asyncio.run(generate())
