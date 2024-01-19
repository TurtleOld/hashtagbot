"""Formatting text for telegram pin message."""
from collections import defaultdict

from sqlalchemy import select
from hashtag_bot.config.bot import bot
from hashtag_bot.models.telegram import CategoryHashTag, HashTag
from hashtag_bot.telegram_bot.common import (
    get_telegram_message_chat,
    create_database_session,
)


async def message_formation(message):
    """Formatting text for telegram pin message."""
    string_keys = ''
    string_keys += '&#128204; Список всех хештегов:\n\n'
    async with await create_database_session() as session:
        _, telegram_message = await get_telegram_message_chat(
            session,
            message,
        )
        result_with_category = defaultdict(list)
        result_with_category.clear()
        result_without_category = []

        hashtag_queryset_without_category = await session.execute(
            select(HashTag)
            .filter(
                HashTag.message_id == telegram_message.id,
                HashTag.category_id.is_(None),
            )
            .distinct()
        )
        result_without_category.extend(
            [
                tag.name
                for tag in hashtag_queryset_without_category.scalars().all()
            ]
        )

        categories = await session.execute(
            select(CategoryHashTag)
            .filter_by(
                message_id=telegram_message.id,
            )
            .distinct()
        )
        result_category = categories.scalars().all()
        for item in result_category:
            hashtag_queryset_with_category = await session.execute(
                select(HashTag).filter_by(category_id=item.id).distinct()
            )
            for item_hashtag in hashtag_queryset_with_category.scalars().all():
                result_with_category[item.name].append(item_hashtag.name)

        for item_key, item_value in result_with_category.items():
            string_value = ' '.join(sorted(set(item_value)))
            string_keys += f'{item_key}\n{string_value}\n\n'
        if result_without_category:
            string_keys += 'No Group\n'
            string_keys += (
                ' '.join(sorted(set(result_without_category))) + '\n\n'
            )

        await bot.pin_chat_message(
            chat_id=message.chat.id,
            message_id=telegram_message.message_id,
            disable_notification=True,
        )
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=telegram_message.message_id,
            text=string_keys,
        )
        await session.commit()
