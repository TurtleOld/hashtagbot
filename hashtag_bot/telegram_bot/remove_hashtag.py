"""Module for functions on removing hashtags"""
from sqlalchemy import delete
from telebot import types
from hashtag_bot.config.bot import bot
from hashtag_bot.models.telegram import HashTag
from hashtag_bot.telegram_bot.common import (
    get_telegram_message_chat,
    create_database_session,
)
from hashtag_bot.telegram_bot.get_db_telegram_info import get_hashtag


async def get_list_hashtag(hashtag: str) -> list:
    """Functing getting list hashtags."""
    return hashtag.split()[1:]


async def remove_hashtag_db(message: types.Message):
    """Function for removing hashtag[s] from database."""
    list_hashtag = await get_list_hashtag(message.text)
    async with create_database_session() as session:
        _, telegram_message = get_telegram_message_chat(
            session,
            message,
        )
        for hashtag in list_hashtag:
            await session.execute(
                delete(HashTag).filter_by(
                    message_id=telegram_message.id, name=hashtag
                )
            )
            await session.commit()
        existing_hashtags = await get_hashtag(session, telegram_message)
        existing_hashtags = ' '.join(
            sorted([hashtag2.name for hashtag2 in set(existing_hashtags)])
        )
        new_text = f'&#128204; Список всех хештегов:\n\n{existing_hashtags}'
        if new_text != existing_hashtags:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=telegram_message.message_id,
                text=new_text,
            )
            await bot.pin_chat_message(
                chat_id=message.chat.id,
                message_id=telegram_message.message_id,
                disable_notification=True,
            )
        await session.commit()


async def remove_hashtag(message: types.Message) -> None:
    """Function for removing hashtag[s]."""
    await remove_hashtag_db(message)
