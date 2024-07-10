import requests
import telebot
import os
import uuid
from datetime import datetime
from .config import TELEGRAM_TOKEN, ALLOWED_TELEGRAM_USERNAMES, FILE_PATH, config
from .github_client import create_or_update_file
from .translator import translate

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# In-memory store for temporary message data
user_data = {
    "first_text": False,
}
current_step = {}


def is_authorized_user(message):
    return message.from_user.username in ALLOWED_TELEGRAM_USERNAMES

def authorized_only(func):
    def wrapper(message):
        if is_authorized_user(message):
            return func(message)
        else:
            bot.reply_to(message, translate("You are not authorized to use this bot."))
    return wrapper

@bot.message_handler(commands=['start'])
@authorized_only
def send_welcome(message):
    bot.reply_to(message, translate("Welcome to the Markdown CMS bot! Use /create to create a new post."))

@bot.message_handler(commands=['create'])
@authorized_only
def create_post(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    current_step[chat_id] = 0
    process_next_step(message)

def process_next_step(message):
    chat_id = message.chat.id
    steps = list(config['fields'].keys())
    if current_step[chat_id] < len(steps):
        current_field = steps[current_step[chat_id]]
        field_info = config['fields'][current_field]
        if field_info['type'] == 'text':
            msg = bot.reply_to(message, f"{translate('Please add ')} {field_info['label']}:")
            bot.register_next_step_handler(msg, process_text_step, current_field)
        elif field_info['type'] == 'file':
            msg = bot.reply_to(message, f"{translate('Please add ')} {field_info['label']}:")
            bot.register_next_step_handler(msg, process_file_step, current_field)
        elif field_info['type'] == 'array_string':
            msg = bot.reply_to(message, f"{translate('Please add ')} {field_info['label']}:")
            user_data[chat_id][current_field] = []
            bot.register_next_step_handler(msg, process_array_string_step, current_field)
        elif field_info['type'] == 'array_object':
            user_data[chat_id][current_field] = []
            process_array_object_step(message, current_field)
        elif field_info['type'] == 'datetime':
            msg = bot.reply_to(message, f"{translate('Please add ')} {field_info['label']}:")
            user_data[chat_id][current_field] = []
            bot.register_next_step_handler(msg, process_date_step, current_field)
        elif field_info['type'] == 'boolean':
            user_data[chat_id][current_field] = []
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(f"✅", f"⛔")
            msg = bot.reply_to(message, field_info['label'], reply_markup=markup)
            bot.register_next_step_handler(msg, process_boolean_step, current_field)
    else:
        bot.reply_to(message, translate('Please confirm to publish the post. Send /confirm to publish or /cancel to discard.'))        

def process_text_step(message, field):
    chat_id = message.chat.id
    user_data[chat_id][field] = message.text

    if user_data['first_text'] == False:
        user_data['first_text'] = True
        slug = f"{message.text.lower().replace(' ', '-')}-{uuid.uuid4()}"
        user_data[chat_id]['slug'] = slug

    current_step[chat_id] += 1
    process_next_step(message)

def process_file_step(message, field):
    chat_id = message.chat.id
    if message.content_type in ['photo', 'document', 'audio']:
        if message.content_type == 'photo':
            file_info = bot.get_file(message.photo[-1].file_id)
        elif message.content_type == 'document':
            file_info = bot.get_file(message.document.file_id)
        elif message.content_type == 'audio':
            file_info = bot.get_file(message.audio.file_id)

        file = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_info.file_path}")
        
        file_ext = os.path.splitext(file_info.file_path)[1]
        filename = f"{uuid.uuid4()}{file_ext}"
        with open(filename, "wb") as file_content:
            file_content.write(file.content)

        field_info = config['fields'][field]
        create_or_update_file(file_path=f"{field_info['folder']}/{filename}", content=file.content)
        
        user_data[chat_id][field] = f"{field_info['folder'].replace('public/', '')}/{filename}"
        if os.path.exists(filename):
            os.remove(filename)

        current_step[chat_id] += 1
        process_next_step(message)
    else:
        msg = bot.reply_to(message, translate("Please send a valid file (photo, document, audio)."))
        bot.register_next_step_handler(msg, process_file_step, field)

def process_array_string_step(message, field):
    chat_id = message.chat.id
    user_data[chat_id][field].append(message.text)
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(f"✅", f"⛔")
    msg = bot.reply_to(message, translate("Add another?"), reply_markup=markup)
    bot.register_next_step_handler(msg, add_more_strings_step, field)

def add_more_strings_step(message, field):
    chat_id = message.chat.id
    if message.text == f"✅":
        msg = bot.reply_to(message, f"{translate("Please send one more.")}")
        bot.register_next_step_handler(msg, process_array_string_step, field)
    else:
        current_step[chat_id] += 1
        process_next_step(message)

def process_array_object_step(message, field):
    chat_id = message.chat.id
    obj_fields = config['fields'][field]['object_fields']
    user_data[chat_id][field].append({})

    first_obj_field = list(obj_fields.keys())[0]
    msg = bot.reply_to(message, f"{translate("Please send the")} {obj_fields[first_obj_field]['label']}.")
    bot.register_next_step_handler(msg, process_object_field_step, field, first_obj_field)

def process_object_field_step(message, field, obj_field):
    chat_id = message.chat.id
    user_data[chat_id][field][-1][obj_field] = message.text
    obj_fields = config['fields'][field]['object_fields']
    if obj_field == list(obj_fields.keys())[-1]:
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(f"✅", f"⛔")
        msg = bot.reply_to(message, translate("Add another entry?"), reply_markup=markup)
        bot.register_next_step_handler(msg, add_more_objects_step, field)
    else:
        next_obj_field = list(obj_fields.keys())[list(obj_fields.keys()).index(obj_field) + 1]
        msg = bot.reply_to(message, f"{translate("Please send the")} {obj_fields[next_obj_field]['label']}.")
        bot.register_next_step_handler(msg, process_object_field_step, field, next_obj_field)

def add_more_objects_step(message, field):
    chat_id = message.chat.id
    if message.text == f"✅":
        process_array_object_step(message, field)
    else:
        current_step[chat_id] += 1
        process_next_step(message)

def process_boolean_step(message, field):
    chat_id = message.chat.id
    user_data[chat_id][field] = (message.text == f"✅")
   
    current_step[chat_id] += 1
    process_next_step(message)

def process_date_step(message, field):
    chat_id = message.chat.id
    try:
        date_obj = datetime.strptime(message.text, "%Y-%m-%d %H:%M:%S")
        user_data[chat_id][field] = date_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
        bot.reply_to(message, translate("Date set successfully."))
        current_step[chat_id] += 1
        process_next_step(message)    

    except ValueError:
        msg = bot.reply_to(message, translate("Invalid date format. Please use YYYY-MM-DD HH:MM:SS."))
        bot.register_next_step_handler(msg, process_date_step, field)
    except Exception as e:
        msg = bot.reply_to(message, f"{translate("Error setting date")}: {str(e)}")
        bot.register_next_step_handler(msg, process_date_step, field)

@bot.message_handler(commands=['confirm'])
@authorized_only
def confirm_post(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        post_data = user_data[chat_id]

        content = "---\n"
        for field, value in post_data.items():
            if isinstance(value, list):
                content += f"{field}:\n"
                for item in value:
                    if isinstance(item, dict):
                        for idx, (k, v) in enumerate(item.items()):
                            if idx == 0:
                                content += f"  - {k}: {v}\n"
                            else:
                                content += f"    {k}: {v}\n"
                    else:
                        content += f"  - {item}\n"
            else:
                content += f"{field}: {value}\n"
        content += "---\n"

        try:
            slug = post_data.get('slug', uuid.uuid4())
            create_or_update_file(
                file_path=f"{FILE_PATH}{slug}.md",
                content=content,
            )
            bot.reply_to(message, f"{translate("New post created successfully!")}")
            del user_data[chat_id]
            del current_step[chat_id]
        except Exception as e:
            bot.reply_to(message, f"{translate("Failed to create new post:")} {e}")
    else:
        bot.reply_to(message, translate('No post to confirm. Please use /create to start creating a new post.'))

@bot.message_handler(commands=['cancel'])
@authorized_only
def cancel_post(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        del user_data[chat_id]
        del current_step[chat_id]
    bot.reply_to(message, translate('Post creation cancelled.'))

def start_bot():
    bot.polling()

if __name__ == '__main__':
    start_bot()
