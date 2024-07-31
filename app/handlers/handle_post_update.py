from urllib.parse import urlparse
from app.bot_instance import bot
from app.utils import telegram_authorized_only
from app.services.translator import translate
from app.handlers.handle_post_create import process_next_step
from app.temp_memory import user_data, current_step

@bot.message_handler(commands=['update'])
@telegram_authorized_only
def update_post(message):
    chat_id = message.chat.id
    user_data["first_text"] = True
    user_data[chat_id] = {}
    current_step[chat_id] = 0
    bot.send_message(chat_id, translate("Please provide the URL of the entry you want to update:"))
    bot.register_next_step_handler(message, process_url_step)

def process_url_step(message):
    chat_id = message.chat.id
    url = message.text
    user_data[chat_id]['slug'] = extract_slug(url)
    process_next_step(message)

def extract_slug(url):
    path = urlparse(url).path
    slug = path.rstrip('/').split('/')[-1]
    return slug

def register_post_update_handler(bot):
    bot.message_handler(commands=['update'])(lambda message: update_post(message))
