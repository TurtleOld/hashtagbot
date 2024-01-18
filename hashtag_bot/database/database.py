"""Settings database."""

import os
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv


load_dotenv()
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')

DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'  # pylint: disable=line-too-long


class Base(
    AsyncAttrs,
    DeclarativeBase,
):  # pylint: disable=too-few-public-methods
    """Init Base Class Database."""

    pass  # pylint: disable=unnecessary-pass
