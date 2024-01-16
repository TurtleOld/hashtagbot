from sqlalchemy import select

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
) -> list:
    hashtags = []
    for item_hashtag in hashtag_list:
        hashtag = await session.execute(
            select(HashTag)
            .filter(
                HashTag.name == item_hashtag,
                HashTag.message_id == telegram_message.id,
            )
            .distinct()
        )
        if not hashtag.scalars().all():
            new_hashtag = HashTag(
                name=item_hashtag.lower(), message=telegram_message
            )
            session.add(new_hashtag)
            await session.commit()
            hashtags.append(new_hashtag)
    return hashtags
