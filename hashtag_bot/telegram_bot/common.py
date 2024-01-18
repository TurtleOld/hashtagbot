"""Module commin logic."""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from hashtag_bot.database.database import DATABASE_URL
from hashtag_bot.telegram_bot.get_db_telegram_info import (
    get_telegram_chat,
    get_telegram_message,
)


async def create_database_session():
    """Create database session."""
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        return session


async def get_telegram_message_chat(session, message):
    """Common function for getting telegram chat and message from database."""
    telegram_chat = await get_telegram_chat(session, message)
    telegram_message = await get_telegram_message(
        session,
        telegram_chat.id,
    )
    return telegram_chat, telegram_message
