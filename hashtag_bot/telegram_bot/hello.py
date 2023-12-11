import asyncio

from telebot import types

from hashtag_bot.config.logger import logger
from hashtag_bot.config.bot import hashtag_bot


@logger.catch
@hashtag_bot.message_handler(commands=['start'])
async def start_message(message: types.Message) -> None:
    await hashtag_bot.reply_to(message, message.text)


def start_bot():
    asyncio.run(hashtag_bot.polling(non_stop=True, restart_on_change=True))
