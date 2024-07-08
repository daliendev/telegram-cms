import telebot
from .config import TELEGRAM_TOKEN
from .github_client import create_or_update_file
from .config import FILE_PATH, ALLOWED_TELEGRAM_USERNAMES

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# In-memory store for temporary message data
user_data = {}

def is_authorized_user(message):
    return message.from_user.username in ALLOWED_TELEGRAM_USERNAMES

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_authorized_user(message):
        bot.reply_to(message, "Welcome to the Markdown CMS bot! Use /create to create a new post.")
    else:
        bot.reply_to(message, "You are not authorized to use this bot.")

@bot.message_handler(commands=['create'])
def create_post(message):
    if is_authorized_user(message):
        user_data[message.chat.id] = {}
        msg = bot.reply_to(message, "Please send the title for the new post.")
        bot.register_next_step_handler(msg, process_title_step)
    else:
        bot.reply_to(message, "You are not authorized to use this bot.")

def process_title_step(message):
    if is_authorized_user(message):
        try:
            chat_id = message.chat.id
            title = message.text
            user_data[chat_id]['title'] = title
            msg = bot.reply_to(message, 'Please send the content for the new post.')
            bot.register_next_step_handler(msg, process_content_step)
        except Exception as e:
            bot.reply_to(message, 'Oops! Something went wrong.')
    else:
        bot.reply_to(message, "You are not authorized to use this bot.")

def process_content_step(message):
    if is_authorized_user(message):
        try:
            chat_id = message.chat.id
            content = message.text
            user_data[chat_id]['content'] = content
            msg = bot.reply_to(message, 'Please confirm to publish the post. Send /confirm to publish or /cancel to discard.')
        except Exception as e:
            bot.reply_to(message, 'Oops! Something went wrong.')
    else:
        bot.reply_to(message, "You are not authorized to use this bot.")

@bot.message_handler(commands=['confirm'])
def confirm_post(message):
    if is_authorized_user(message):
        chat_id = message.chat.id
        if chat_id in user_data and 'content' in user_data[chat_id]:
            title = user_data[chat_id]['title']
            content = user_data[chat_id]['content']
            slug = title.lower().replace(' ', '-')

            post_data = {
                'title': title,
                'content': content,
                'slug': slug,
                'description': '',
                'draft': '',
                'tags': '',
            }

            content = "---\n"
            for field, value in post_data.items():
                content += f"{field}: {value}\n"
            content += "---\n"
            content += post_data.get('content', '')

            file_path = f"{FILE_PATH}{slug}.md"

            try:
                create_or_update_file(file_path=file_path, content=content)
                bot.reply_to(message, 'New post created successfully!')
                del user_data[chat_id]
            except Exception as e:
                bot.reply_to(message, f'Failed to create new post: {e}')
        else:
            bot.reply_to(message, 'No post to confirm. Please use /create to start creating a new post.')
    else:
        bot.reply_to(message, "You are not authorized to use this bot.")

@bot.message_handler(commands=['cancel'])
def cancel_post(message):
    if is_authorized_user(message):
        chat_id = message.chat.id
        if chat_id in user_data:
            del user_data[chat_id]
        bot.reply_to(message, 'Post creation cancelled.')
    else:
        bot.reply_to(message, "You are not authorized to use this bot.")

def start_bot():
    bot.polling()
