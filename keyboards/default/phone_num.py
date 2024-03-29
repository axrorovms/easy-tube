from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.translate import btn_lang


def phone_num_btn(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(btn_lang['request_phone'][lang], request_contact=True))
    return keyboard
