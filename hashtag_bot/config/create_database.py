from hashtag_bot.database.database import create_db
from hashtag_bot.models.telegram import TelegramChat, TelegramMessage, HashTag


def create_database():
    create_db()
