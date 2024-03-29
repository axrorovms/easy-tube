from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.translate import btn_lang


def settings_btn(lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.row(KeyboardButton(btn_lang["change_lang"][lang]))
    btn.row(KeyboardButton(btn_lang["cancel"][lang]))
    return btn
