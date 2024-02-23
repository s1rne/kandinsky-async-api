# kandinsky-api-requests

api для использования нейросети kandinsky 2.2

ВНИМАНИЕ: Проект работал со старой версией kandinsky. Проект заброшен (возможно временно) и не работает с новой версией kandinsky

**Как использовать:**

### 1. text2image

```
model = FusionBrainApi()


async def generate():
    img_bytes = await model.text2image("котик", style="CYBERPUNK")
    img = Image.open(img_bytes)
    img.save('cat_cyberpunk.jpg')


if __name__ == '__main__':
    asyncio.run(generate())
```

Все стили можно посмотреть в `FusionBrainApi().styles`:

```
async def read_styles():
    for style in model.styles:
        print(style)
        print("\n")
```
