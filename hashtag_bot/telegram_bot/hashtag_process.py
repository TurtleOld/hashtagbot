from icecream import ic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)
from telebot import types
from hashtag_bot.config.logger import logger
from hashtag_bot.config.bot import bot
from hashtag_bot.database.database import DATABASE_URL
from hashtag_bot.models.telegram import (
    HashTag,
    TelegramMessage,
    TelegramChat,
    AdminChat,
)


@logger.catch
@bot.message_handler(commands=['start'])
async def start_message(message: types.Message) -> None:
    await bot.reply_to(message, message.text)


@logger.catch
async def get_telegram_chat(session, message: types.Message) -> TelegramChat:
    telegram_chat = await session.execute(
        select(TelegramChat).filter_by(chat_id=message.chat.id)
    )
    return telegram_chat.scalar_one_or_none()


@logger.catch
async def get_telegram_message(session, telegram_chat_id) -> TelegramMessage:
    result = await session.execute(
        select(TelegramMessage).filter_by(chat_id=telegram_chat_id)
    )
    ic(result)
    return result.scalar_one_or_none()


@logger.catch
async def record_telegram_chat(session, telegram_chat) -> None:
    telegram_chat = TelegramChat(chat_id=telegram_chat)
    session.add(telegram_chat)
    await session.commit()


@logger.catch
async def record_telegram_message(
    session,
    telegram_message_id: int,
    telegram_chat,
) -> None:
    ic(telegram_chat)
    ic()
    telegram_message = TelegramMessage(
        message_id=telegram_message_id,
        chat=telegram_chat,
    )
    session.add(telegram_message)
    await session.commit()


@logger.catch
async def record_hashtags_database(
    session,
    hashtag_list,
    telegram_message,
) -> list[HashTag]:
    hashtags = [
        HashTag(name=name_hashtag.lower(), message=telegram_message)
        for name_hashtag in hashtag_list
    ]
    session.add_all(hashtags)
    await session.commit()
    return hashtags


async def existing_hashtag(session, telegram_message: TelegramMessage):
    result = await session.execute(
        select(HashTag).filter_by(message_id=telegram_message.id)
    )
    return result.scalars()


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
                ic(telegram_chat)
                ic(telegram_chat.chat_id)
                telegram_message = await get_telegram_message(
                    session,
                    telegram_chat.id,
                )
                ic(telegram_message)

                await bot.pin_chat_message(
                    chat_id=telegram_chat.chat_id,
                    message_id=telegram_message.message_id,
                    disable_notification=True,
                )
            else:
                existing_hashtags = await existing_hashtag(
                    session, telegram_message
                )
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


@logger.catch
@bot.channel_post_handler(func=lambda message: message.text)
async def process_hashtag_channel(message: types.Message) -> None:
    engine = create_async_engine(
        f'postgresql+asyncpg://{DATABASE_URL}',
        echo=True,
    )

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    await process_hashtags(async_session, message)


ALLOWED_USERS = ['219008465']


@logger.catch
@bot.message_handler(func=lambda message: message.text)
async def process_hashtag_group(message: types.Message) -> None:
    engine = create_async_engine(
        f'postgresql+asyncpg://{DATABASE_URL}',
        echo=True,
    )

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    await process_hashtags(async_session, message)


@logger.catch
async def start_bot():
    return await bot.infinity_polling()
