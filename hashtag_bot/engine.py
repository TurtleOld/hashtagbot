import asyncio
from hashtag_bot.config.logger import logger
from hashtag_bot.telegram_bot.telegram_command import start_bot


@logger.catch
def main():
    asyncio.run(start_bot())


if __name__ == '__main__':
    main()
