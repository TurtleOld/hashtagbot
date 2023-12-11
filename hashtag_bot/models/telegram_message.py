from sqlalchemy import Column, Integer

from hashtag_bot.models.database import Base


class TelegramMessage(Base):
    __tablename__ = "telegram_message"

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
