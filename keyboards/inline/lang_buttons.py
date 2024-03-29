from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

langs = InlineKeyboardMarkup(row_width=2)
langs.insert(InlineKeyboardButton("O'zbek 🇺🇿", callback_data="lang_uz"))
langs.insert(InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru"))
langs.insert(InlineKeyboardButton("English 🇬🇧", callback_data="lang_en"))
