import os.path

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncAttrs,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_async_engine(f'postgresql+asyncpg://{DATABASE_URL}', echo=True)

Session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def init_db() -> None:
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)


async def get_session() -> None:
    async_session = Session()
    async with async_session() as session:
        yield session
