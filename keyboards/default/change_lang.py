from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def change_lang_btn(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("🇺🇿 O'zbek tili"))
    keyboard.add(KeyboardButton("🇷🇺 Русский язык"))
    keyboard.add(KeyboardButton("🇬🇧 English"))
    return keyboard
