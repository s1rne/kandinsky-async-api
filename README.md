# kandinsky-api-requests

**Асионхронное** api для использования нейросети kandinsky 3.0

ВНИМАНИЕ: После изменнеия структуры сайта, сделана работа только для api версии. Планируется "взломать" использование web версии программно.

**Как использовать:**
###### *полный пример можно посмотреть в tests.py*

### 1. text2image

```
model = FusionBrainApi()


async def generate():
    result = await model.text2image("котик", style="ANIME")
    if result["error"]:
        print("Error:")
        print(result["data"])
    else:
        img = Image.open(result["data"])
        img.save('cat_anime.jpg')
        print("Done!")


if __name__ == '__main__':
    asyncio.run(generate())
```

Все стили можно посмотреть в `await FusionBrainApi().get_styles()`:

```
async def read_styles():
    for style in await model.get_styles():
        print(style, end="\n\n")
```


![Пример генерации](https://github.com/s1rne/kandinsky-async-api/blob/main/cat_anime.jpg)
