# **kandinsky-api-requests**

**Асинхронное** api для использования kandinsky 3.1 в своих проектах

## **Как использовать:**
##### Установка: 
```
pip install AsyncKandinsky
```

### Для инициализации FusionBrainApi можно использовать keys или данные аккаунта:
 + api_key и secret_key:
   + **!!! Ключи создаются во вкладке api (https://fusionbrain.ai/keys/)**
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
    try:
        result = await model.text2image("котик", style="ANIME", art_gpt=True)
        # новый параметр art_gpt - это инструмент для автоматического улучшения промпта => улучшение качества картинки
    except ValueError as e:
        print(f"Error:\t{e}")
    else:
        with open("cat_anime_img.png", "wb") as f:
            f.write(result.getvalue())
        print("Done!")
```

### 2. text2animation
```
async def generate():
    # описания для двух сцен
    try:
        result = await model.text2video("котик бежит по полю")
        # заготовленных стилей нет
    except ValueError as e:
        print(f"Error:\t{e}")
    else:
        with open("cat_anime_video.mp4", "wb") as f:
            f.write(result.getvalue())
        print("Done!")
```

### 3. text2video
```
async def generate():
    try:
        result = await model.text2animation(["котик бежит по полю", "котик пьёт воду из речки"])
        # заготовленных стилей нет
    except ValueError as e:
        print(f"Error:\t{e}")
    else:
        with open("cat_anime_animation.mp4", "wb") as f:
            f.write(result.getvalue())
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
