
from sqlalchemy import Column, Integer, String

from hashtag_bot.models.database import Base


class HashTag(Base):
    __tablename__ = "hashtag"

    id = Column(Integer, primary_key=True)
    name = Column(String)
