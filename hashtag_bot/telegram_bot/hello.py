import asyncio

from icecream import ic
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
def get_telegram_message(session: Session, chat_id: int) -> TelegramMessage:
    return (
        session.query(TelegramMessage)
        .join(TelegramMessage.chat)
        .filter(TelegramChat.chat_id == chat_id)
        .first()
    )


@logger.catch
def record_telegram_message(
    session: Session,
    telegram_message_id: int,
    telegram_chat,
) -> TelegramMessage:
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
) -> list[HashTag]:
    hashtags = [
        HashTag(name=name_hashtag.lower(), message=telegram_message)
        for name_hashtag in hashtag_list
    ]
    session.add_all(hashtags)
    telegram_message.hashtags.extend(hashtags)
    session.merge(telegram_message)
    session.commit()
    return hashtags


@logger.catch
@bot.channel_post_handler(func=lambda message: message.text)
async def process_hashtag_channel(message: types.Message) -> None:
    if '#' in message.text:
        hashtags = [
            name_hashtag.lower()
            for name_hashtag in message.text.split()
            if name_hashtag.startswith('#')
        ]
        with Session() as session:
            telegram_message = get_telegram_message(session, message.chat.id)
            if not telegram_message:
                sent_hashtags = await bot.send_message(
                    message.chat.id, ' '.join([hashtag for hashtag in hashtags])
                )
                telegram_chat = record_telegram_chat(session, message)
                telegram_message = record_telegram_message(
                    session,
                    sent_hashtags.message_id,
                    telegram_chat,
                )

                await bot.pin_chat_message(
                    chat_id=message.chat.id,
                    message_id=telegram_message.message_id,
                    disable_notification=True,
                )
            else:
                existing_hashtags = (
                    session.query(HashTag)
                    .distinct()
                    .join(HashTag.message)
                    .filter(
                        TelegramMessage.message_id
                        == telegram_message.message_id
                    )
                    .all()
                )
                existing_hashtags = ' '.join(
                    [hashtag2.name for hashtag2 in existing_hashtags]
                )

                combined_hashtags = set(existing_hashtags.split()).union(
                    set(hashtags)
                )

                new_text = ' '.join(sorted(combined_hashtags))

                if new_text != existing_hashtags:
                    await bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=telegram_message.message_id,
                        text=new_text,
                    )
                session.commit()
            record_hashtags_database(session, hashtags, telegram_message)


@logger.catch
@bot.message_handler(func=lambda message: message.text)
async def process_hashtag_group(message: types.Message) -> None:
    if '#' in message.text:
        hashtags = [
            name_hashtag.lower()
            for name_hashtag in message.text.split()
            if name_hashtag.startswith('#')
        ]
        with Session() as session:
            telegram_message = get_telegram_message(session, message.chat.id)
            if not telegram_message:
                sent_hashtags = await bot.send_message(
                    message.chat.id, ' '.join([hashtag for hashtag in hashtags])
                )
                telegram_chat = record_telegram_chat(session, message)
                telegram_message = record_telegram_message(
                    session,
                    sent_hashtags.message_id,
                    telegram_chat,
                )

                await bot.pin_chat_message(
                    chat_id=message.chat.id,
                    message_id=telegram_message.message_id,
                    disable_notification=True,
                )
            else:
                existing_hashtags = (
                    session.query(HashTag)
                    .distinct()
                    .join(HashTag.message)
                    .filter(
                        TelegramMessage.message_id
                        == telegram_message.message_id
                    )
                    .all()
                )
                existing_hashtags = ' '.join(
                    [hashtag2.name for hashtag2 in existing_hashtags]
                )

                combined_hashtags = set(existing_hashtags.split()).union(
                    set(hashtags)
                )

                new_text = ' '.join(sorted(combined_hashtags))

                if new_text != existing_hashtags:
                    await bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=telegram_message.message_id,
                        text=new_text,
                    )
                session.commit()
            record_hashtags_database(session, hashtags, telegram_message)


def start_bot() -> None:
    asyncio.run(bot.infinity_polling())
