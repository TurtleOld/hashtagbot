from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from hashtag_bot.database.database import Base


class TelegramMessage(Base):
    __tablename__ = "telegram_message"

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    chat_id = Column(Integer, ForeignKey('telegram_chat.id'))
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
    chat_id = Column(Integer)
    message = relationship(
        "TelegramMessage",
        uselist=False,
        back_populates="chat",
    )
    admin_user_chat = relationship(
        'AdminChat',
        uselist=True,
        back_populates="chat",
    )


class HashTag(Base):
    __tablename__ = "hashtag"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    message_id = Column(Integer, ForeignKey("telegram_message.id"))
    message = relationship(
        "TelegramMessage",
        back_populates="hashtags",
    )


class AdminChat(Base):
    __tablename__ = "admin_chat"

    id = Column(Integer, primary_key=True)
    admin_user = Column(String)
    chat_id = Column(Integer, ForeignKey('telegram_chat.id'))
    chat = relationship(
        "TelegramChat",
        back_populates="admin_user_chat",
        uselist=True,
        single_parent=True,
    )
