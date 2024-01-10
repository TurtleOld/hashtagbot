from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from telebot import types

from hashtag_bot.config.logger import logger
from hashtag_bot.config.bot import bot
from hashtag_bot.database.database import DATABASE_URL
from hashtag_bot.telegram_bot.hashtag_process import process_hashtags


@logger.catch
@bot.message_handler(commands=['start'])
async def start_message(message: types.Message) -> None:
    await bot.reply_to(message, message.text)


@logger.catch
@bot.channel_post_handler(commands=['start'])
async def start_message_channel(message: types.Message) -> None:
    await bot.reply_to(message, message.text)


@logger.catch
@bot.message_handler(commands=['delete'])
async def start_message(message: types.Message) -> None:
    await bot.reply_to(message, message.text)


@logger.catch
@bot.channel_post_handler(commands=['delete'])
async def start_message_channel(message: types.Message) -> None:
    await bot.reply_to(message, message.text)


@logger.catch
@bot.channel_post_handler(func=lambda message: message.text)
async def process_hashtag_channel(message: types.Message) -> None:
    engine = create_async_engine(DATABASE_URL)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    await process_hashtags(async_session, message)


@logger.catch
@bot.message_handler(func=lambda message: message.text)
async def process_hashtag_group(message: types.Message) -> None:
    admins = await bot.get_chat_administrators(message.chat.id)
    for admin in admins:
        if (
            admin.status in ['administrator', 'creator']
            or admin.user.username == 'hashgettag_bot'
            or admin.user.username == 'gethashtag_bot'
        ):
            engine = create_async_engine(DATABASE_URL)

            async_session = async_sessionmaker(engine, expire_on_commit=False)

            await process_hashtags(async_session, message)


@logger.catch
async def start_bot():
    return await bot.infinity_polling()
