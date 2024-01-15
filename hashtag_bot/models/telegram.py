from sqlalchemy import Column, Integer, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship

from hashtag_bot.database.database import Base


class TelegramMessage(Base):
    __tablename__ = "telegram_message"

    id = Column(Integer, primary_key=True)
    message_id = Column(BigInteger)
    chat_id = Column(BigInteger, ForeignKey('telegram_chat.id'))
    hashtags = relationship("HashTag", back_populates="message")
    chat = relationship(
        "TelegramChat",
        back_populates="message",
        uselist=False,
        single_parent=True,
    )


class TelegramChat(Base):
    __tablename__ = "telegram_chat"

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger)
    message = relationship(
        "TelegramMessage",
        uselist=False,
        back_populates="chat",
    )


class HashTag(Base):
    __tablename__ = "hashtag"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = relationship(
        'CategoryHashTag',
        back_populates='hashtags',
    )
    message_id = Column(BigInteger, ForeignKey("telegram_message.id"))
    message = relationship(
        "TelegramMessage",
        back_populates="hashtags",
    )


class CategoryHashTag(Base):
    __tablename__ = 'category_hashtag'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    message_id = Column(BigInteger, ForeignKey("telegram_message.id"))
    message = relationship(
        "TelegramMessage",
        back_populates="category_hashtag",
    )
