from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from telebot import types

from hashtag_bot.config.logger import logger
from hashtag_bot.config.bot import bot
from hashtag_bot.database.database import DATABASE_URL
from hashtag_bot.telegram_bot.add_group import add_group
from hashtag_bot.telegram_bot.add_hashtag_in_group import add_hashtag_group
from hashtag_bot.telegram_bot.formation import message_formation
from hashtag_bot.telegram_bot.hashtag_process import process_hashtags
from hashtag_bot.telegram_bot.remove_hashtag import remove_hashtag


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
async def delete_hashtag_group(message: types.Message) -> None:
    await remove_hashtag(message)


@logger.catch
@bot.channel_post_handler(commands=['delete'])
async def delete_hashtag_channel(message: types.Message) -> None:
    await remove_hashtag(message)


@logger.catch
@bot.message_handler(commands=['category'])
async def add_category_group(message: types.Message) -> None:
    await add_group(message)


@logger.catch
@bot.channel_post_handler(commands=['category'])
async def add_category_channel(message: types.Message) -> None:
    await add_group(message)


@logger.catch
@bot.message_handler(commands=['hashtag'])
async def handler_add_hashtag_group(message: types.Message) -> None:
    await add_hashtag_group(message)


@logger.catch
@bot.channel_post_handler(commands=['hashtag'])
async def handler_add_hashtag_channel(message: types.Message) -> None:
    await add_hashtag_group(message)


@logger.catch
@bot.message_handler(commands=['commit'])
async def commit_group(message: types.Message) -> None:
    await message_formation(message)


@logger.catch
@bot.channel_post_handler(commands=['commit'])
async def commit_channel(message: types.Message) -> None:
    await message_formation(message)


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
    administrator = [
        admin.status
        for admin in admins
        if admin.status
        in [
            'admin',
            'creator',
        ]
    ]
    username = [
        admin.user.username
        for admin in admins
        if admin.user.username in ['hashgettag_bot', 'gethashtag_bot']
    ]
    if administrator or username:
        engine = create_async_engine(DATABASE_URL)

        async_session = async_sessionmaker(engine, expire_on_commit=False)

        await process_hashtags(async_session, message)


@logger.catch
async def start_bot():
    return await bot.infinity_polling()
