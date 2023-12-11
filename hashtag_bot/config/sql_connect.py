import sqlalchemy as db

engine = db.create_engine('sqlite:///../sql/database/hashtag_bot.db')
connection = engine.connect()

metadata = db.MetaData()

# Create table the Message for save message_id from Telegram Chat
message = db.Table(
    'telegram_message',
    metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('message_id', db.Integer),
)

metadata.create_all(engine)
