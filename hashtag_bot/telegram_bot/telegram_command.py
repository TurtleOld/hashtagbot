"""Module telegram command."""
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
@bot.message_handler(commands=['start', 'help'])
async def start_message(message: types.Message) -> None:
    """
    Function handler messages from group.
    /start command handler function.
    """
    text_for_user: str = ''.join(
        (
            '&#128075; Привет!\nТебя приветствует бот ',
            'для хранения хештегов в\n&#128204;закрепленном сообщении.\n\n',
            'Ты можешь меня добавить в &#128483;канал или &#129340;группу ',
            'и я начну собирать все хештеги, которые ты посылаешь.\n',
            'Я отвечаю только в личной переписке, владельцу и\\или ',
            'администраторам канала\\группы.\n\n',
            'Давай познакомлю тебя с тем, что я имею.\n',
            'Когда я вижу сообщение с хештегом,',
            ' я беру его и сохраняю в базу данных',
            ', и записываю в сообщение, закрепив его.\n',
            'Закрепленное сообщение сохраняется в базе данных ',
            'и туда добавляются новые хештеги.\n',
            '/category - позволяет добавлять категорию для хештегов\n',
            'Пример:\n<code>/category name_category</code>, '
            'можно указывать название '
            'категории через пробел, '
            'но тогда слова \"заключаются в кавычки\"\n',
            'Чтобы добавить хештеги в категорию, '
            'нужно использовать команду /add_hashtag_category\nПример:\n',
            '<code>/add_hashtag_category name_category #hashtag\n</code>',
            'Можно удалить хештег(и). Для этого используется команда /remove\n',
            'Пример:\n<code>/remove #hashtag #newhashtag</code>\n',
            'Чтобы увидеть это сообщение ещё раз, потребуется команда ',
            '/start или /help',
        )
    )
    await bot.send_message(message.chat.id, text_for_user)


@logger.catch
@bot.channel_post_handler(commands=['start'])
async def start_message_channel(message: types.Message) -> None:
    """
    Function handler messages from channel.
    /start command handler function.
    """
    await bot.reply_to(message, message.text)


@logger.catch
@bot.message_handler(commands=['delete'])
async def delete_hashtag_group(message: types.Message) -> None:
    """
    Function handler messages from group.
    Handler function for deleting hashtags.
    """
    await remove_hashtag(message)


@logger.catch
@bot.channel_post_handler(commands=['delete'])
async def delete_hashtag_channel(message: types.Message) -> None:
    """
    Function handler messages from channel.
    Handler function for deleting hashtags.
    """
    await remove_hashtag(message)


@logger.catch
@bot.message_handler(commands=['category'])
async def add_category_group(message: types.Message) -> None:
    """
    Function handler messages from channel.
    Handler function for adding categories.
    """
    await add_group(message)


@logger.catch
@bot.channel_post_handler(commands=['category'])
async def add_category_channel(message: types.Message) -> None:
    """
    Function handler messages from channel.
    Handler function for adding categories.
    """
    await add_group(message)


@logger.catch
@bot.message_handler(commands=['add_hashtag_category'])
async def handler_add_hashtag_group(message: types.Message) -> None:
    """
    Function handler messages from channel.
    Handler function for adding hashtags to a category.
    """
    await add_hashtag_group(message)


@logger.catch
@bot.channel_post_handler(commands=['add_hashtag_category'])
async def handler_add_hashtag_channel(message: types.Message) -> None:
    """
    Function handler messages from channel.
    Handler function for adding hashtags to a category.
    """
    await add_hashtag_group(message)


@logger.catch
@bot.message_handler(commands=['commit'])
async def commit_group(message: types.Message) -> None:
    """
    Function handler messages from group.
    The function is needed in order for the text in the pinned message
    to be formed according to a template.
    """
    await message_formation(message)


@logger.catch
@bot.channel_post_handler(commands=['commit'])
async def commit_channel(message: types.Message) -> None:
    """
    Function handler messages from channel.
    The function is needed in order for the text in the pinned message
    to be formed according to a template.
    """
    await message_formation(message)


@logger.catch
@bot.channel_post_handler(func=lambda message: message.text)
async def process_hashtag_channel(message: types.Message) -> None:
    """Function handler messages from channel."""
    engine = create_async_engine(DATABASE_URL)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    await process_hashtags(async_session, message)


@logger.catch
@bot.message_handler(func=lambda message: message.text)
async def process_hashtag_group(message: types.Message) -> None:
    """
    Function handler messages from group.
    Only administrators can write messages with hashtags.
    """
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
    """Function for start telegram bot"""
    return await bot.infinity_polling()
