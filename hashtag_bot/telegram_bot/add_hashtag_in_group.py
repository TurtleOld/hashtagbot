import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from telebot import types

from hashtag_bot.config.bot import bot
from hashtag_bot.database.database import DATABASE_URL
from hashtag_bot.models.telegram import CategoryHashTag, HashTag
from hashtag_bot.telegram_bot.get_db_telegram_info import (
    get_telegram_chat,
    get_telegram_message,
)


async def add_hashtag_group(message: types.Message):
    input_user = message.text.split('"')
    category_name = input_user[1]
    hashtags = [hashtag.strip() for hashtag in input_user[2:]][0].split()
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        telegram_chat = await get_telegram_chat(session, message)
        telegram_message = await get_telegram_message(session, telegram_chat.id)
        category_queryset = await session.execute(
            select(CategoryHashTag).filter_by(
                name=category_name,
                message_id=telegram_message.id,
            )
        )
        category = category_queryset.scalars().one()

        if category.name:
            for hashtag_item in hashtags:
                hashtag_queryset = await session.execute(
                    select(HashTag).filter_by(
                        name=hashtag_item,
                        message_id=telegram_message.id,
                    )
                )
                result_hashtag = hashtag_queryset.scalars().all()
                result_hashtag[0].category_id = category.id
                string_hashtags = ' '.join(hashtags)
                await bot.send_message(
                    message.chat.id,
                    f'Hashtag[s]: {string_hashtags} added to {category.name} group',
                )
                await session.commit()
