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
    print(message.message_id + 1)
    with Session() as session:
        select_message_id = select(TelegramMessage.message_id)
        message_id = session.execute(select_message_id).first()
        insert_message_result = []
        if not message_id:
            insert_message = TelegramMessage(message_id=message.message_id + 1)
            insert_message_result.append(insert_message)
            print(insert_message)
            print(insert_message_result)
            session.add(insert_message)
            session.commit()

        await bot.pin_chat_message(
            chat_id=message.chat.id,
            message_id=message_id[0],
            disable_notification=True,
        )
        print(insert_message_result)
        print(message_id)
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id[0],
            text=', '.join(hashtag_list_message),
        )



def start_bot() -> None:
    asyncio.run(bot.infinity_polling())
