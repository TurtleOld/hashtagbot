"""Module for logging."""
from loguru import logger

logger.add(
    'debug.json',
    level='DEBUG',
    rotation='1 week',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    compression='zip',
    serialize=True,
    colorize=True,
)
