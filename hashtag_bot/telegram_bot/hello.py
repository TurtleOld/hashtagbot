import asyncio

from telebot import types

from hashtag_bot.config.logger import logger
from hashtag_bot.config.bot import bot


@logger.catch
@bot.message_handler(commands=['start'])
async def start_message(message: types.Message) -> None:
    await bot.reply_to(message, message.text)


@logger.catch
@bot.message_handler(func=lambda message: message.text)
async def get_message_id(message: types.Message) -> None:
    hashtag_list_message = []
    message_split = message.text.split()
    for mess in message_split:
        if mess.startswith('#'):
            hashtag_list_message.append(mess)
    await bot.send_message(message.chat.id, ', '.join(hashtag_list_message))
    print(message)


def start_bot() -> None:
    asyncio.run(bot.infinity_polling())
