import asyncio

from hashtag_bot.config.logger import logger
from hashtag_bot.telegram_bot.hashtag_process import start_bot


@logger.catch
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
    loop.close()


if __name__ == '__main__':
    main()
