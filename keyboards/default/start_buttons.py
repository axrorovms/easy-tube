from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.translate import btn_lang as btn_lang_translate


def get_main_menu(lang):
    res = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_lang = btn_lang_translate['main_menu']
    res.row(
        KeyboardButton(btn_lang['video_download'][lang]), KeyboardButton(btn_lang['download_video_music'][lang])
    )
    res.row(
        KeyboardButton(btn_lang['summarize_video'][lang]), KeyboardButton(btn_lang['get_channel_info'][lang])
    )
    res.row(
        KeyboardButton(btn_lang['settings'][lang]), KeyboardButton(btn_lang['donate'][lang])
    )
    return res


def get_main_menu_admin(lang):
    btn_lang = btn_lang_translate['main_menu']
    return get_main_menu(lang).row(
        KeyboardButton(btn_lang['view_users'][lang])
    )
