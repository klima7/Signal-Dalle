import os

import deepl


SOURCE_LANG = os.getenv('LANGUAGE')
API_KEY = os.getenv('DEEPL_API_KEY')

translator = deepl.Translator(API_KEY)


def to_english(text):
    if SOURCE_LANG in ['EN-GB', 'EN-US']:
        return text
    
    result = translator.translate_text(
        text,
        source_lang=SOURCE_LANG,
        target_lang='EN-US'
    )
    return result.text
