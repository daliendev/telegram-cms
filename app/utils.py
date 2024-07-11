from functools import wraps
from .config import ALLOWED_TELEGRAM_USERNAMES

def is_authorized_user(message) -> bool:
    """
    Check if the user is authorized to use the bot.
    """
    return message.from_user.username in ALLOWED_TELEGRAM_USERNAMES

def telegram_authorized_only(func):
    """
    Decorator to restrict access to authorized users only.
    """
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        if is_authorized_user(message):
            return func(message, *args, **kwargs)
        else:
            return None
    return wrapper