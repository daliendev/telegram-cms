from deep_translator import GoogleTranslator
from ..config import config

def translate(sentence):
    target = config['language']
    source = 'en'
    if target == source:
        return sentence
    return GoogleTranslator(source=source, target=target).translate(sentence)