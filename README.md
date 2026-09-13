# Space Telegram

Скрипты скачивают фотографии космоса из NASA и Wikimedia Commons и публикуют их в Telegram-канал.

## Установка

Установите зависимости:

```bash
pip install -r requirements.txt
```

Создайте файл `.env` в корне проекта:

```env
NASA_API_KEY=ваш_токен_NASA
TELEGRAM_BOT_TOKEN=токен_telegram_бота
TELEGRAM_CHAT_ID=id_telegram_канала
PUBLISH_INTERVAL_HOURS=4
PROXY_URL=socks5h://IP:PORT
```

`NASA_API_KEY` — API-токен NASA.

`TELEGRAM_BOT_TOKEN` — токен Telegram-бота.

`TELEGRAM_CHAT_ID` — идентификатор Telegram-канала.

`PUBLISH_INTERVAL_HOURS` — интервал между публикациями в часах. По умолчанию используется 4 часа.

`PROXY_URL` — адрес SOCKS5-прокси. Если прокси не используется, переменную можно оставить пустой или не указывать.

Пример SOCKS5-прокси:

```env
PROXY_URL=socks5h://127.0.0.1:1080
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

Можно указать количество фотографий:

```bash
python fetch_nasa_apod.py --count 30
```

## Скачать фотографии NASA EPIC

```bash
python fetch_nasa_epic.py
```

Можно указать количество фотографий:

```bash
python fetch_nasa_epic.py --count 5
```

## Опубликовать одну фотографию

Опубликовать случайную фотографию из директории `images`:

```bash
python publish_photo.py
```

Опубликовать конкретную фотографию:

```bash
python publish_photo.py images/photo.jpg
```

## Автоматическая публикация фотографий

```bash
python publish_photos.py
```

Скрипт публикует все фотографии из директории `images` в случайном порядке и после окончания начинает публикацию заново.

По умолчанию фотография публикуется раз в 4 часа.

Интервал задаётся через `.env`:

```env
PUBLISH_INTERVAL_HOURS=4
```

Можно указать другую директорию с фотографиями:

```bash
python publish_photos.py other_images
```