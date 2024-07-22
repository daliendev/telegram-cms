from app.bot_instance import bot
from .utils import telegram_authorized_only
from .services.translator import translate
from .handlers.handle_post_create import register_post_create_handler

@bot.message_handler(commands=['start'])
@telegram_authorized_only
def send_welcome(message):
    bot.reply_to(message, translate("Welcome to the Markdown CMS bot! Use /create to create a new entry or /update + URL or /delete + URL to manage existent ones."))

@bot.message_handler(func=lambda message: True)
@telegram_authorized_only
def handle_default(message):
    send_welcome(message)

def start_bot():
    register_post_create_handler(bot)
    bot.polling()

if __name__ == '__main__':
    start_bot()
