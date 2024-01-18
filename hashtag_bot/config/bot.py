"""Settings telegram bot."""
import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

load_dotenv()
token = os.getenv('TOKEN_TELEGRAM_BOT')
bot = AsyncTeleBot(token, parse_mode='html')
