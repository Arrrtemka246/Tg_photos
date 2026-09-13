# Space Telegram

Скрипты скачивают фотографии космоса из NASA и Wikimedia Commons и публикуют их в Telegram-канал.

## Установка

Установите зависимости:

```bash
pip install -r requirements.txt
```

Создайте файл `.env`:

```env
NASA_API_KEY=ваш_токен_NASA
TELEGRAM_BOT_TOKEN=токен_telegram_бота
TELEGRAM_CHAT_ID=id_telegram_канала
PUBLISH_INTERVAL_HOURS=4
```

## Скачать фотографии SpaceX

```bash
python fetch_spacex_images.py
```

Можно указать свой поисковый запрос:

```bash
python fetch_spacex_images.py --query "Falcon 9 launch"
```

## Скачать фотографии NASA APOD

```bash
python fetch_nasa_apod.py
```

## Скачать фотографии NASA EPIC

```bash
python fetch_nasa_epic.py
```

## Автоматическая публикация фотографий

```bash
python publish_photos.py
```

Скрипт публикует фотографии из директории `images`.

Интервал публикации задаётся переменной окружения:

```env
PUBLISH_INTERVAL_HOURS=4
```

По умолчанию фотография публикуется раз в 4 часа.