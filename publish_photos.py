import argparse
import os
import random
import time
from pathlib import Path

from dotenv import load_dotenv
from telegram import Bot


DEFAULT_IMAGES_DIRECTORY = 'images'
DEFAULT_PUBLISH_INTERVAL_HOURS = 4
MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = MINUTES_IN_HOUR * SECONDS_IN_MINUTE


def publish_photos(
    bot,
    chat_id,
    images_dir,
    delay,
):
    while True:
        image_paths = [
            path
            for path in images_dir.iterdir()
            if path.is_file()
        ]

        random.shuffle(image_paths)

        for image_path in image_paths:
            with open(image_path, 'rb') as photo:
                bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                )

            time.sleep(delay)


def main():
    load_dotenv()

    telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

    publish_interval_hours = float(
        os.getenv(
            'PUBLISH_INTERVAL_HOURS',
            str(DEFAULT_PUBLISH_INTERVAL_HOURS),
        )
    )

    parser = argparse.ArgumentParser(
        description=(
            'Публикует фотографии из директории '
            'в Telegram-канал в бесконечном цикле.'
        ),
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default=DEFAULT_IMAGES_DIRECTORY,
        help=(
            'Директория с фотографиями. '
            'По умолчанию используется images.'
        ),
    )

    args = parser.parse_args()

    project_dir = Path(__file__).parent
    images_dir = project_dir / args.directory

    delay = (
        publish_interval_hours
        * SECONDS_IN_HOUR
    )

    bot = Bot(token=telegram_token)

    publish_photos(
        bot,
        telegram_chat_id,
        images_dir,
        delay,
    )


if __name__ == '__main__':
    main()