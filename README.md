# **kandinsky-api-requests**

**Асинхронное** api для использования kandinsky 3.0 в своих проектах

## **Как использовать:**
##### Установка: 
```
pip install AsyncKandinsky
```

### Для инициализации FusionBrainApi можно использовать keys или данные аккаунта:
 + api_key и secret_key:
   + **!!! Ключи создаются в вкладке api (https://fusionbrain.ai/keys/)**
   + быстрый и простой способ генерации 
   + не самое лучше качество генерации
 + почта и пароль - данные от уже созданного аккаунта:
   + **!!! Обязательно нужен уже зарегистрированный аккаунт**
   + в такой версии будет доступна генерация: **видео / анимации / больше стилей**
   + лучшее качество генерации

```
model = FusionBrainApi(ApiApi("Сюда свой api_key", "Сюда свой secret_key"))
# Любой способ на выбор
model = FusionBrainApi(ApiWeb("Ваша почта", "Ваш пароль"))
```

#
###### *Полные примеры можно посмотреть в tests.py (GitHub)*


### 1. text2image
```
async def generate():
    result = await model.text2image("котик", style="ANIME")
    if result["error"]:
        print("Error:")
        print(result["data"])
    else:
        with open("cat_anime_img.png", "wb") as f:
            f.write(result["data"].getvalue())
        print("Done!")
```

### 2. text2animation
```
async def generate():
    # описания для двух сцен
    result = await model.text2animation(["котик бежит по полю", "котик пьёт воду из речки"])
    # Стиль придётся самому вписывать
    if result["error"]:
        print("Error:")
        print(result["data"])
    else:
        with open("cat_anime_animation.mp4", "wb") as f:
            f.write(result["data"].getvalue())
        print("Done!")
```

### 3. text2video
```
async def generate():
    result = await model.text2video("котик бежит по полю")
    # Стиль придётся самому вписывать
    if result["error"]:
        print("Error:")
        print(result["data"])
    else:
        with open("cat_anime_video.mp4", "wb") as f:
            f.write(result["data"].getvalue())
        print("Done!")
```

#
Все стили можно посмотреть в `await FusionBrainApi().get_styles()`:

```
async def read_styles():
    for style in await model.get_styles():
        print(style)
```

![Пример генерации](https://github.com/s1rne/kandinsky-async-api/blob/main/cat_anime.jpg)
