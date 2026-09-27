import argparse
import os
import random
from pathlib import Path

from dotenv import load_dotenv
from telegram import Bot


DEFAULT_IMAGES_DIRECTORY = 'images'


def main():
    load_dotenv()

    telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

    parser = argparse.ArgumentParser(
        description=(
            'Публикует указанную или случайную '
            'фотографию в Telegram-канал.'
        ),
    )
    parser.add_argument(
        'image',
        nargs='?',
        help=(
            'Путь к фотографии. '
            'Если не указан, выбирается случайная '
            'фотография из директории images.'
        ),
    )

    args = parser.parse_args()

    project_dir = Path(__file__).parent

    if args.image:
        image_path = Path(args.image)
    else:
        images_dir = project_dir / DEFAULT_IMAGES_DIRECTORY
        image_paths = [
            path
            for path in images_dir.iterdir()
            if path.is_file()
        ]
        image_path = random.choice(image_paths)

    bot = Bot(token=telegram_token)

    with open(image_path, 'rb') as photo:
        bot.send_photo(
            chat_id=telegram_chat_id,
            photo=photo,
        )


if __name__ == '__main__':
    main()