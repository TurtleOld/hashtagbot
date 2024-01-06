import asyncio
from hashtag_bot.config.logger import logger
from hashtag_bot.telegram_bot.hashtag_process import start_bot


@logger.catch
async def async_main():
    ...


if __name__ == '__main__':
    # asyncio.run(process_hashtag_channel)
    asyncio.run(start_bot())
