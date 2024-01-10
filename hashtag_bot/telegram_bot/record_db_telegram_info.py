from hashtag_bot.config.logger import logger
from hashtag_bot.models.telegram import TelegramMessage, HashTag, TelegramChat


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
