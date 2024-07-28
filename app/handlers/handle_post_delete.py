from urllib.parse import urlparse
from app.bot_instance import bot
from app.utils import telegram_authorized_only
from app.services.translator import translate
from app.temp_memory import user_data, current_step
from app.services.github_client import delete_file
from app.config import FILE_PATH

@bot.message_handler(commands=['delete'])
@telegram_authorized_only
def delete_post(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    current_step[chat_id] = 0
    bot.send_message(chat_id, translate("Please provide the URL of the entry you want to delete:"))
    bot.register_next_step_handler(message, process_url_step)

def process_url_step(message):
    chat_id = message.chat.id
    url = message.text
    user_data[chat_id]['slug'] = extract_slug(url)
    bot.send_message(chat_id, translate("Are you sure you want to delete this post? (✅/⛔)"))
    bot.register_next_step_handler(message, confirm_delete_step)

def confirm_delete_step(message):
    chat_id = message.chat.id
    confirmation = message.text.lower()
    if confirmation == f"✅":
        slug = user_data[chat_id]['slug']
        result = delete_file(
            file_path=f"{FILE_PATH}{slug}.md",
            )
        bot.send_message(chat_id, translate(result))
    else:
        bot.send_message(chat_id, translate("Deletion canceled."))

def extract_slug(url):
    path = urlparse(url).path
    slug = path.rstrip('/').split('/')[-1]
    return slug


def register_post_delete_handler(bot):
    bot.message_handler(commands=['delete'])(lambda message: delete_post(message))
