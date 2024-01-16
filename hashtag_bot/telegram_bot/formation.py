from collections import defaultdict

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from hashtag_bot.database.database import DATABASE_URL
from hashtag_bot.models.telegram import CategoryHashTag, HashTag
from hashtag_bot.telegram_bot.get_db_telegram_info import (
    get_telegram_chat,
    get_telegram_message,
)


async def message_formation(message):
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        telegram_chat = await get_telegram_chat(session, message)
        telegram_message = await get_telegram_message(session, telegram_chat.id)
        categories = await session.execute(
            select(CategoryHashTag)
            .filter_by(
                message_id=telegram_message.id,
            )
            .distinct()
        )
        result_with_category = defaultdict(list)
        result_without_category = []
        string_keys = ''
        result_category = categories.scalars().all()
        for item in result_category:
            hashtag_queryset_with_category = await session.execute(
                select(HashTag).filter_by(category_id=item.id).distinct()
            )
            for item_hashtag in hashtag_queryset_with_category.scalars().all():
                result_with_category[item.name].append(item_hashtag.name)

            hashtag_queryset_without_category = await session.execute(
                select(HashTag).filter(HashTag.category_id.is_(None)).distinct()
            )
            result_without_category.extend(
                [
                    tag.name
                    for tag in hashtag_queryset_without_category.scalars().all()
                ]
            )
        for item_key, item_value in result_with_category.items():
            string_value = ' '.join(item_value)
            string_keys += f'{item_key}\n{string_value}\n\n'
        if result_without_category:
            string_keys += 'No Group\n'
            string_keys += ' '.join(result_without_category) + '\n\n'

        print(string_keys)
        await session.commit()
        # hashtag_queryset = await session.execute(
        #     select(HashTag).filter_by(category=result_category)
        # )
        # result_hashtag = hashtag_queryset.scalars().all()
        # print(result_hashtag)
