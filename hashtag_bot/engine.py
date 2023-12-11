import os
import asyncio
from config.create_database import create_database
from hashtag_bot.telegram_bot.hello import start_bot
from models.database import DATABASE_NAME


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
    loop.close()
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_database()
