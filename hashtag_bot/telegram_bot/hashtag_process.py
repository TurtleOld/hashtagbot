from collections import OrderedDict

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)
from telebot import types, asyncio_helper
from hashtag_bot.config.logger import logger
from hashtag_bot.config.bot import bot

from hashtag_bot.telegram_bot.get_db_telegram_info import (
    get_telegram_chat,
    get_telegram_message,
)
from hashtag_bot.telegram_bot.record_db_telegram_info import (
    record_telegram_chat,
    record_telegram_message,
    record_hashtags_database,
)


@logger.catch
async def process_hashtags(
    async_session: async_sessionmaker[AsyncSession],
    message: types.Message,
) -> None:
    if '#' in message.text:
        hashtags = [
            name_hashtag.lower()
            for name_hashtag in message.text.split()
            if name_hashtag.startswith('#')
        ]
        hashtags = list(OrderedDict.fromkeys(hashtags))

        async with async_session() as session:
            telegram_chat = await get_telegram_chat(session, message)
            if not telegram_chat:
                await record_telegram_chat(
                    session,
                    message.chat.id,
                )

            telegram_chat = await get_telegram_chat(session, message)
            telegram_message = await get_telegram_message(
                session,
                telegram_chat.id,
            )
            if not telegram_message:
                sent_hashtags = await bot.send_message(
                    message.chat.id,
                    '&#128204; Список всех хештегов:\n\n'
                    + ' '.join([hashtag for hashtag in sorted(set(hashtags))]),
                )
                await record_telegram_message(
                    session,
                    sent_hashtags.message_id,
                    telegram_chat,
                )

                telegram_chat = await get_telegram_chat(session, message)
                telegram_message = await get_telegram_message(
                    session,
                    telegram_chat.id,
                )
            try:
                await bot.pin_chat_message(
                    chat_id=telegram_chat.chat_id,
                    message_id=telegram_message.message_id,
                    disable_notification=True,
                )
            except asyncio_helper.ApiTelegramException:
                sent_hashtags = await bot.send_message(
                    message.chat.id,
                    '&#128204; Список всех хештегов:\n\n'
                    + ' '.join([hashtag for hashtag in sorted(set(hashtags))]),
                )
                await record_telegram_message(
                    session,
                    sent_hashtags.message_id,
                    telegram_chat,
                )

                telegram_chat = await get_telegram_chat(session, message)
                telegram_message = await get_telegram_message(
                    session,
                    telegram_chat.id,
                )
            await record_hashtags_database(
                session,
                hashtags,
                telegram_message,
            )
