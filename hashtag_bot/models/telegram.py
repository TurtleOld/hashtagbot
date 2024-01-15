from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column

from hashtag_bot.database.database import Base


class TelegramChat(Base):
    __tablename__ = "telegram_chat"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = Column(BigInteger)

    message: Mapped['TelegramMessage'] = relationship(back_populates="chat")


class TelegramMessage(Base):
    __tablename__ = "telegram_message"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = Column(BigInteger)

    chat_id: Mapped[int] = mapped_column(
        ForeignKey('telegram_chat.id'),
        nullable=True,
    )
    chat: Mapped['TelegramChat'] = relationship(back_populates="message")

    categories: Mapped['CategoryHashTag'] = relationship(
        back_populates='message',
    )

    hashtags: Mapped[List['HashTag']] = relationship()


class HashTag(Base):
    __tablename__ = "hashtag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = Column(String)

    message_id: Mapped[int] = mapped_column(
        ForeignKey("telegram_message.id"),
        nullable=True,
    )
    message: Mapped['TelegramMessage'] = relationship(back_populates="hashtags")

    category_id: Mapped[int] = mapped_column(
        ForeignKey('category_hashtag.id'),
        nullable=True,
    )
    category: Mapped['CategoryHashTag'] = relationship(
        back_populates='hashtags'
    )


class CategoryHashTag(Base):
    __tablename__ = 'category_hashtag'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = Column(String, nullable=True)

    message_id: Mapped[int] = mapped_column(
        ForeignKey("telegram_message.id"),
        nullable=True,
    )
    message: Mapped['TelegramMessage'] = relationship(
        back_populates="categories",
    )
    hashtags: Mapped[List['HashTag']] = relationship()
