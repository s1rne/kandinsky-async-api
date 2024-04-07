# kandinsky-api-requests

**Асинхронное** api для использования kandinsky 3.0

ВНИМАНИЕ: После изменения структуры сайта, сделана api только по их ключам. Планируется отревёрсить использование web версии программно.

### **Как использовать:**
##### Установка: ```pip install AsyncKandinsky```

### Для инициализации FusionBrainApi можно использовать keys или данные аккаунта:
 + api_key и secret_key:
   + **!!! Ключи создаются в вкладке api (https://fusionbrain.ai/keys/)**
   + быстрый и простой способ генерации 
   + не самое лучше качество генерации
 + почта и пароль - данные от уже созданного аккаунта:
   + **!!! Обязательно нужен уже зарегистрированный аккаунт**
   + в такой версии будет доступна генерация: **видео / анимации / больше стилей** {В процесса разработки}
   + лучшее качество генерации
###### *Полный пример можно посмотреть в tests.py (GitHub)*


### 1. text2image

```
model = FusionBrainApi(ApiApi(api_key, secret_key))
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


if __name__ == '__main__':
    asyncio.run(generate())
```

Все стили можно посмотреть в `await FusionBrainApi().get_styles()`:

```
async def read_styles():
    for style in await model.get_styles():
        print(style)
```

![Пример генерации](https://github.com/s1rne/kandinsky-async-api/blob/main/cat_anime.jpg)
