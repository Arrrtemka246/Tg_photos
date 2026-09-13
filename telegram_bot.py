import os

from dotenv import load_dotenv
from telegram import Bot


load_dotenv()

telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

bot = Bot(token=telegram_token)

bot.send_message(
    chat_id=telegram_chat_id,
    text='Привет! Это тестовая публикация.',
)