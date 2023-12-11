from loguru import logger

logger.add(
    'debug.json',
    level='DEBUG',
    rotation='week',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    compression='zip',
    serialize=True,
)
