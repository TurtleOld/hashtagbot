import asyncio

from sqlalchemy import select, ChunkedIteratorResult, Row
from telebot import types

from hashtag_bot.config.logger import logger
from hashtag_bot.config.bot import bot
from hashtag_bot.database.database import Session
from hashtag_bot.models.telegram import HashTag, TelegramMessage, TelegramChat


@logger.catch
@bot.message_handler(commands=['start'])
async def start_message(message: types.Message) -> None:
    await bot.reply_to(message, message.text)


@logger.catch
def record_telegram_chat(session, message: types.Message) -> TelegramChat:
    telegram_chat = (
        session.query(TelegramChat).filter_by(chat_id=message.chat.id).first()
    )
    if not telegram_chat:
        telegram_chat = TelegramChat(chat_id=message.chat.id)
        session.add(telegram_chat)
        session.commit()
    return telegram_chat


@logger.catch
def get_telegram_message(session: Session, message) -> TelegramMessage:
    return (
        session.query(TelegramMessage)
        .filter_by(message_id=message.message_id)
        .first()
    )


@logger.catch
def record_telegram_message(
    session: Session,
    telegram_message_id: int,
    telegram_chat,
) -> TelegramMessage:
    if not telegram_message_id:
        telegram_message = TelegramMessage(
            message_id=telegram_message_id,
            chat=telegram_chat,
        )
        session.add(telegram_message)
        session.commit()
        return telegram_message


@logger.catch
def record_hashtags_database(
    session: Session(),
    hashtag_list,
    telegram_message,
) -> None:
    hashtags = [
        HashTag(name=name_hashtag, message=telegram_message)
        for name_hashtag in hashtag_list
    ]
    print(hashtags)
    telegram_message.hashtags.extend(hashtags)
    session.merge(telegram_message)
    session.commit()


# @logger.catch
# def record_message_id_database(session: Session, message_id: int) -> None:
#     insert_message_id = TelegramMessage(message_id=message_id)
#     session.add(insert_message_id)
#     session.commit()


#
#
# @logger.catch
# def process_message_ids(session: Session) -> tuple[ChunkedIteratorResult, Row]:
#     select_hashtags = select(HashTag.name).distinct()
#     hashtags = session.execute(select_hashtags)
#     select_message_id = select(TelegramMessage.message_id)
#     message_ids = session.execute(select_message_id).first()
#     return hashtags, message_ids
#
#
# @logger.catch
# def record_message_id_database(session: Session, message_id: int) -> None:
#     insert_message_id = TelegramMessage(message_id=message_id)
#     session.add(insert_message_id)
#     session.commit()


@logger.catch
@bot.channel_post_handler(func=lambda message: message.text)
async def process_hashtag_channel(message: types.Message) -> None:
    if '#' in message.text:
        hashtags = [
            name_hashtag
            for name_hashtag in message.text.split()
            if name_hashtag.startswith('#')
        ]
        print(hashtags)
        with Session() as session:
            telegram_chat = record_telegram_chat(session, message)
            print(telegram_chat)
            telegram_message = get_telegram_message(session, message)
            print(telegram_message)
            if not telegram_message:
                sent_hashtags = await bot.send_message(
                    message.chat.id, " ".join([tag for tag in hashtags])
                )
                telegram_message = record_telegram_message(
                    session,
                    sent_hashtags.message_id,
                    telegram_chat,
                )
            record_hashtags_database(session, hashtags, telegram_message)
            await bot.pin_chat_message(
                chat_id=message.chat.id,
                message_id=sent_hashtags.message_id,
                disable_notification=True,
            )

            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=int(telegram_message[0]),
                text=", ".join([tag[0] for tag in hashtags]),
            )
            session.commit()


# @logger.catch
# @bot.message_handler(func=lambda message: message.text)
# async def process_hashtag_group(message: types.Message) -> None:
#     record_hashtags_database(message)
#     with Session() as session:
#         record_chat_id(session, message.chat.id)
#         hashtags, message_ids = process_message_ids(session)
#         if not message_ids:
#             sent_hashtags = await bot.send_message(
#                 message.chat.id, ", ".join([tag[0] for tag in hashtags])
#             )
#             record_message_id_database(session, sent_hashtags.message_id)
#             await bot.pin_chat_message(
#                 chat_id=message.chat.id,
#                 message_id=sent_hashtags.message_id,
#                 disable_notification=True,
#             )
#
#         await bot.edit_message_text(
#             chat_id=message.chat.id,
#             message_id=int(message_ids[0]),
#             text=", ".join([tag[0] for tag in hashtags]),
#         )


def start_bot() -> None:
    asyncio.run(bot.infinity_polling())
