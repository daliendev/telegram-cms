import yaml
from deep_translator import GoogleTranslator
from ..config import config

def translate(sentence):
    translations = load_translations()
    if sentence in translations:
        return translations[sentence]
    else:
        target = config['language']
        source = 'en'
        if target == source:
            return sentence
        translated_sentence = GoogleTranslator(source=source, target=target).translate(sentence)
        save_translation(sentence, translated_sentence)
        return translated_sentence
    
def load_translations():
    try:
        with open('translations.yaml', 'r') as file:
            translations = yaml.safe_load(file)
            if translations is None:
                translations = {}
    except FileNotFoundError:
        translations = {}
    return translations

def save_translation(original_message, translated_message):
    translations = load_translations()
    translations[original_message] = translated_message
    with open('translations.yaml', 'w') as file:
        yaml.safe_dump(translations, file)
