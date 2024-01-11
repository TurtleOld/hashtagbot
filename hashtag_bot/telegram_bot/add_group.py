from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from telebot import types

from hashtag_bot.database.database import DATABASE_URL
from hashtag_bot.models.telegram import HashTag, CategoryHashTag
from hashtag_bot.telegram_bot.get_db_telegram_info import (
    get_telegram_chat,
    get_telegram_message,
)


async def add_hashtag_group(message: types.Message):
    list_hashtag = message.text.split()[2:]
    group_name = message.text.split()[1]
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        telegram_chat = await get_telegram_chat(session, message)
        telegram_message = await get_telegram_message(session, telegram_chat.id)
        for hashtag in list_hashtag:
            result = await session.execute(
                select(HashTag).filter_by(
                    message_id=telegram_message.id,
                    name=hashtag,
                )
            )
            await session.commit()
            category_hashtag = CategoryHashTag(
                name=group_name,
                hashtag_id=result.scalar_one_or_none().id,
            )
            session.add(category_hashtag)
            await session.commit()
