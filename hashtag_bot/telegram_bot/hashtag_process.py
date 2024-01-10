from icecream import ic
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)
from telebot import types
from hashtag_bot.config.logger import logger
from hashtag_bot.config.bot import bot
from hashtag_bot.telegram_bot.get_db_telegram_info import (
    get_telegram_chat,
    get_telegram_message,
    get_hashtag,
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

                await bot.pin_chat_message(
                    chat_id=telegram_chat.chat_id,
                    message_id=telegram_message.message_id,
                    disable_notification=True,
                )
            else:
                existing_hashtags = await get_hashtag(session, telegram_message)
                existing_hashtags = ' '.join(
                    [hashtag2.name for hashtag2 in set(existing_hashtags)]
                )
                combined_hashtags = set(existing_hashtags.split()).union(
                    set(hashtags)
                )

                new_text = '&#128204; Список всех хештегов:\n\n' + ' '.join(
                    sorted(combined_hashtags)
                )
                telegram_chat = await get_telegram_chat(session, message)
                telegram_message = await get_telegram_message(
                    session,
                    telegram_chat.id,
                )
                if new_text != existing_hashtags:
                    await bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=telegram_message.message_id,
                        text=new_text,
                    )
                await session.commit()
            await record_hashtags_database(
                session,
                hashtags,
                telegram_message,
            )
