# kandinsky-api-requests

Асионхронное api для использования нейросети kandinsky 2.2

ВНИМАНИЕ: После изменнеия структуры сайта, сделана работа только для api версии. Планируется "взломать" использование web версии программно.

**Как использовать:**

### 1. text2image

```
model = FusionBrainApi()


async def generate():
    img_bytes = await model.text2image("котик", style="ANIME")
    img = Image.open(img_bytes)
    img.save('cat_anime.jpg')


if __name__ == '__main__':
    asyncio.run(generate())
```

Все стили можно посмотреть в `await FusionBrainApi().get_styles()`:

```
async def read_styles():
    for style in await model.get_styles():
        print(style, end="\n\n")
```
