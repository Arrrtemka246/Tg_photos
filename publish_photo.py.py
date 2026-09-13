import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import Bot


load_dotenv()

telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

bot = Bot(token=telegram_token)

project_dir = Path(__file__).parent
images_dir = project_dir / 'images'
image_path = next(images_dir.iterdir())

with open(image_path, 'rb') as photo:
    bot.send_photo(
        chat_id=telegram_chat_id,
        photo=photo,
    )