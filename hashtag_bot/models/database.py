import os.path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_NAME = 'database/hashtag_bot.sqlite'

engine = create_engine(f'sqlite:///{os.path.abspath(DATABASE_NAME)}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)
