import argparse
import os
import random
import time
from pathlib import Path

from dotenv import load_dotenv
from telegram import Bot


def publish_photos(bot, chat_id, images_dir, delay):
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
        os.getenv('PUBLISH_INTERVAL_HOURS', '4')
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'directory',
        nargs='?',
        default='images',
        help='Директория с фотографиями',
    )
    args = parser.parse_args()

    project_dir = Path(__file__).parent
    images_dir = project_dir / args.directory

    delay = publish_interval_hours * 60 * 60

    bot = Bot(token=telegram_token)

    publish_photos(
        bot,
        telegram_chat_id,
        images_dir,
        delay,
    )


if __name__ == '__main__':
    main()