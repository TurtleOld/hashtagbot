"""Module for adding hashtag[s] to category"""
from sqlalchemy import select
from telebot import types

from hashtag_bot.config.bot import bot
from hashtag_bot.models.telegram import CategoryHashTag, HashTag
from hashtag_bot.telegram_bot.common import (
    create_database_session,
    get_telegram_message_chat,
)


async def add_hashtag_group(message: types.Message):
    """Function for adding hashtag[s] to category"""
    input_user = message.text.split('"')
    category_name = input_user[1]
    hashtags = [hashtag.strip() for hashtag in input_user[2:]][0].split()
    async with create_database_session() as session:
        _, telegram_message = get_telegram_message_chat(
            session,
            message,
        )
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
                    f'Hashtag[s]: {string_hashtags} '
                    f'added to {category.name} group',
                )
                await session.commit()
