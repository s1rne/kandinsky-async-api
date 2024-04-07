# kandinsky-api-requests

**Асинхронное** api для использования kandinsky 3.0

ВНИМАНИЕ: После изменения структуры сайта, сделана api только по их ключам. Планируется отревёрсить использование web версии программно.

### **Как использовать:**
##### Установка: pip install AsyncKandinsky

### Для инициализации FusionBrainApi можно использовать keys или данные аккаунта:
 + api_key и secret_key - их надо создать во вкладе api (https://fusionbrain.ai/keys/):
   + быстрый и простой способ генерации 
 + почта и пароль - данные от уже созданного аккаунта {пока в разработке}:
   + в такой версии будет доступна генерация: **видео / анимации / больше стилей**
###### *Полный пример можно посмотреть в tests.py (GitHub)*


### 1. text2image

```
model = FusionBrainApi(ApiApi(api_key, secret_key))


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
