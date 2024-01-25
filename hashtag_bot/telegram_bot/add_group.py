"""Module with func for adding category."""
import re

from sqlalchemy import select
from telebot import types
from hashtag_bot.config.bot import bot
from hashtag_bot.models.telegram import CategoryHashTag
from hashtag_bot.telegram_bot.common import (
    get_telegram_message_chat,
    create_database_session,
)
from hashtag_bot.telegram_bot.formation import message_formation


async def add_group(message: types.Message):
    """Function for adding category."""
    input_user = message.text
    category_name = re.findall(r'"[^"]*"|\S+', input_user)[1].replace('"', '')
    async with create_database_session() as session:
        _, telegram_message = await get_telegram_message_chat(
            session,
            message,
        )
        category = await session.execute(
            select(CategoryHashTag).filter_by(
                name=category_name,
                message_id=telegram_message.id,
            )
        )
        if not category.all():
            category_hashtag = CategoryHashTag(
                name=category_name.replace('"', ''),
                message_id=telegram_message.id,
            )
            session.add(category_hashtag)
            await session.commit()
            await bot.send_message(
                message.chat.id,
                f'Категория "{category_name}" добавлена.',
            )
            await message_formation(message)
        else:
            await bot.send_message(
                message.chat.id,
                f'Категория "{category_name}" уже существует.',
            )
            await message_formation(message)
