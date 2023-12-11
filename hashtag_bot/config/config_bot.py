import os

from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv()
token = os.getenv('TOKEN_TELEGRAM_BOT')
hashtag_bot = TeleBot(token, parse_mode='html')
