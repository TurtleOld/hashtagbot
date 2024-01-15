import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from telebot import types

from hashtag_bot.config.bot import bot
from hashtag_bot.database.database import DATABASE_URL
from hashtag_bot.models.telegram import CategoryHashTag
from hashtag_bot.telegram_bot.get_db_telegram_info import (
    get_telegram_chat,
    get_telegram_message,
)


async def add_hashtag_group(message: types.Message):
    input_user = message.text
    category_name = re.findall(r'"[^"]*"|\S+', input_user)[1]
    print(category_name)
    # category_name = [word for word in message.text.split('"')][1]
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        telegram_chat = await get_telegram_chat(session, message)
        telegram_message = await get_telegram_message(session, telegram_chat.id)
        category = await session.execute(
            select(CategoryHashTag).filter_by(
                name=category_name,
                message_id=telegram_message.id,
            )
        )
        if not category.scalar_one_or_none():
            category_hashtag = CategoryHashTag(
                name=category_name,
                message_id=telegram_message.id,
            )
            session.add(category_hashtag)
            await session.commit()
        else:
            await bot.send_message(
                message.chat.id, f'Category "{category_name}" already exists'
            )
