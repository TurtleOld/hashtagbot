"""Module for get telegram information from database."""
from sqlalchemy import select
from telebot import types

from hashtag_bot.config.logger import logger
from hashtag_bot.models.telegram import TelegramMessage, HashTag, TelegramChat


@logger.catch
async def get_telegram_chat(session, message: types.Message) -> TelegramChat:
    """Get queryset with telegram chat from database."""
    telegram_chat = await session.execute(
        select(TelegramChat).filter_by(chat_id=message.chat.id)
    )
    return telegram_chat.scalar_one_or_none()


@logger.catch
async def get_telegram_message(session, telegram_chat_id) -> TelegramMessage:
    """Get queryset with telegram message from database."""
    result = await session.execute(
        select(TelegramMessage).filter_by(chat_id=telegram_chat_id)
    )
    return result.scalar_one_or_none()


async def get_hashtag(session, telegram_message: TelegramMessage):
    """Get queryset with hashtag from database."""
    result = await session.execute(
        select(HashTag).filter_by(message_id=telegram_message.id)
    )
    return result.scalars()
