import asyncio

from sqlalchemy import select
from telebot import types

from hashtag_bot.config.logger import logger
from hashtag_bot.config.bot import bot
from hashtag_bot.models.database import Session
from hashtag_bot.models.telegram_message import TelegramMessage
from hashtag_bot.models.hashtag_list import HashTag


@logger.catch
@bot.message_handler(commands=['start'])
async def start_message(message: types.Message) -> None:
    await bot.reply_to(message, message.text)


@logger.catch
def record_hashtags_database(message):
    if '#' in message.text:
        message_split = message.text.split()
        with Session() as session:
            for mess in message_split:
                if mess.startswith('#'):
                    insert_hashtag = HashTag(name=mess)
                    session.add(insert_hashtag)
                    session.commit()

    
@logger.catch
@bot.message_handler(func=lambda message: message.text)
async def get_message_id(message: types.Message) -> None:
    hashtag_list_message = []
    record_hashtags_database(message)
    with Session() as session:
        select_hashtags = select(HashTag.name).distinct()
        hashtags = session.execute(select_hashtags)
        select_message_id = select(TelegramMessage.message_id)
        message_ids = session.execute(select_message_id).first()
        if not message_ids:
            sent_hashtags = await bot.send_message(message.chat.id, ", ".join([tag[0] for tag in hashtags]))
            insert_message_id = TelegramMessage(message_id=sent_hashtags.message_id)
            session.add(insert_message_id)
            session.commit()
            await bot.pin_chat_message(
                chat_id=message.chat.id,
                message_id=sent_hashtags.message_id,
                disable_notification=True,
            )
        
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=int(message_ids[0]),
            text=", ".join([tag[0] for tag in hashtags]),
        )

        

    #with Session() as session:
    #    select_message_id = select(TelegramMessage.message_id)
    #    message_id = session.execute(select_message_id).first()
    #    insert_message_result = []
    #    print(message_id)
    #    if not message_id:
    #        insert_message = TelegramMessage(message_id=sent_message.message_id)
    #        insert_message_result.append(insert_message)
    #        print(insert_message)
    #        print(insert_message_result)
    #        session.add(insert_message)
    #        session.commit()#

    #    await bot.pin_chat_message(
    #        chat_id=message.chat.id,
    #        message_id=message_id[0],
    #        disable_notification=True,
    #    )
    #    print(insert_message_result)
    #    print(message_id)
    #    await bot.edit_message_text(
    #        chat_id=message.chat.id,
    #        message_id=message_id[0],
    #        text=', '.join(hashtag_list_message),
    #    )
    #   print(message_id[0])



def start_bot() -> None:
    asyncio.run(bot.infinity_polling())
