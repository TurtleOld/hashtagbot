import os
import asyncio

from hashtag_bot.config.create_database import create_database
from hashtag_bot.models.database import DATABASE_NAME
from hashtag_bot.telegram_bot.hello import start_bot

def main():
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_database()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
    loop.close()
    
if __name__ == '__main__':
    main()
