from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from telebot import types

from hashtag_bot.config.bot import bot
from hashtag_bot.database.database import DATABASE_URL
from hashtag_bot.models.telegram import HashTag
from hashtag_bot.telegram_bot.get_db_telegram_info import (
    get_telegram_chat,
    get_telegram_message,
    get_hashtag,
)


async def get_list_hashtag(hashtag: str) -> list:
    return hashtag.split()[1:]


async def get_hashtag_db(message: types.Message):
    list_hashtag = await get_list_hashtag(message.text)
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        telegram_chat = await get_telegram_chat(session, message)
        telegram_message = await get_telegram_message(
            session,
            telegram_chat.id,
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
    await get_hashtag_db(message)
