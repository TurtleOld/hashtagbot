from sqlalchemy import Column, Integer, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship

from hashtag_bot.database.database import Base


class TelegramChat(Base):
    __tablename__ = "telegram_chat"

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger)
    message_id = Column(BigInteger, ForeignKey('telegram_message.id'))
    message = relationship("TelegramMessage", back_populates="chat")


class TelegramMessage(Base):
    __tablename__ = "telegram_message"

    id = Column(Integer, primary_key=True)
    message_id = Column(BigInteger)
    category_id = Column(
        BigInteger, ForeignKey('category_hashtag.id'), nullable=True
    )
    chat_id = Column(BigInteger, ForeignKey('telegram_chat.id'))

    chat = relationship(
        "TelegramChat", back_populates="message", foreign_keys=[chat_id]
    )
    category = relationship(
        'CategoryHashTag', back_populates='message', foreign_keys=[category_id]
    )
    hashtags = relationship(
        "HashTag", back_populates="message", foreign_keys=[id]
    )


class HashTag(Base):
    __tablename__ = "hashtag"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(
        BigInteger, ForeignKey('category_hashtag.id'), nullable=True
    )
    message_id = Column(BigInteger, ForeignKey("telegram_message.id"))

    category = relationship(
        'CategoryHashTag', back_populates='hashtags', foreign_keys=[category_id]
    )
    message = relationship(
        "TelegramMessage", back_populates="hashtags", foreign_keys=[message_id]
    )


class CategoryHashTag(Base):
    __tablename__ = 'category_hashtag'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)

    messages = relationship(
        "TelegramMessage", back_populates="category", foreign_keys=[id]
    )
    hashtags = relationship(
        "HashTag", back_populates="category", foreign_keys=[id]
    )
