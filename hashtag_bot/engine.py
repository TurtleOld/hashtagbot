from config.config_bot import hashtag_bot


@hashtag_bot.message_handler(commands=['start'])
def send_welcome(message):
    hashtag_bot.send_message(message.chat.id, hashtag_bot)
