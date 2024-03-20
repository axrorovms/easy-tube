from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.translate import btn_lang


def cancel_btn(lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.insert(KeyboardButton(btn_lang["cancel"][lang]))
    return btn
