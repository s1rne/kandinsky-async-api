import asyncio

from PIL import Image

from api import FusionBrainApi


async def main():
    test = FusionBrainApi()
    img_bytes = await test.text2image("Котик", style="CYBERPUNK")
    img = Image.open(img_bytes)
    img.save('cat_cyberpunk.jpg')


if __name__ == '__main__':
    asyncio.run(main())
