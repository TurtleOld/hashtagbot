from hashtag_bot.models.database import create_db
from hashtag_bot.models.telegram_message import TelegramMessage
from hashtag_bot.models.hashtag_list import HashTag


def create_database():
    create_db()
