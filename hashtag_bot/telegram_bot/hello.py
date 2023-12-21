import asyncio

from sqlalchemy import select
from telebot import types

from hashtag_bot.config.logger import logger
from hashtag_bot.config.bot import bot
from hashtag_bot.models.database import Session
from hashtag_bot.models.telegram_message import TelegramMessage


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
    session: Session = Session()
    select_message_id = select(TelegramMessage.message_id)
    message_id = (
        session.query(TelegramMessage)
        .filter(TelegramMessage.message_id == int(message.message_id))
        .scalar_subquery()
    )
    # message_id_text = ''.join(list(message_id))
    session.close()
    print(message.message_id)
    if not list(message_id):
        session: Session = Session()
        insert_message = TelegramMessage(message_id=message.message_id)
        session.add(insert_message)
        session.commit()
        session.close()

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message_id,
        text=', '.join(hashtag_list_message),
    )

    await bot.unpin_all_chat_messages(chat_id=message.chat.id)
    await bot.pin_chat_message(
        chat_id=message.chat.id,
        message_id=select_message_id,
        disable_notification=True,
    )


def start_bot() -> None:
    asyncio.run(bot.infinity_polling())
