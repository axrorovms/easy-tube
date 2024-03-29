from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from data.translate import msg_lang
from keyboards.default.change_lang import change_lang_btn
from keyboards.default.settings import settings_btn
from keyboards.default.start_buttons import get_main_menu_admin, get_main_menu
from loader import dp, db
from states.settings_states import ChangeLang


@dp.message_handler(lambda x: x.text in ("Sozlamalar ⚙️", "Настройки ⚙️", "Settings ⚙️"))
async def all_users(msg: types.Message):
    lang = db.select_user_lang(tg_id=msg.from_user.id)
    txt = msg_lang['settings'][lang[0]]
    btn = settings_btn(lang[0])
    await msg.answer(txt, reply_markup=btn)
    await ChangeLang.first()

@dp.message_handler(state=ChangeLang.action)
async def all_users(msg: types.Message, state: FSMContext):
    lang = db.select_user_lang(tg_id=msg.from_user.id)
    if msg.text in ("Отмена", "Bekor qilish", "Cancel"):
        if str(msg.from_user.id) in ADMINS:
            txt = msg_lang["main_menu"][lang[0]]
            btn = get_main_menu_admin(lang[0])
            await msg.answer(txt, reply_markup=btn)
            await state.finish()
            return
        txt = msg_lang["main_menu"][lang[0]]
        btn = get_main_menu(lang[0])
        await state.finish()
        await msg.answer(txt, reply_markup=btn)
        return
    elif msg.text in ( "Tilni o'zgartirish🔄", "Изменить язык🔄", "Change language🔄"):
        txt = """
        🇺🇿 Tilni tanlang
🇷🇺 Выберите язык
🇬🇧 Choose language
        """
        btn = change_lang_btn(lang[0])
        await msg.answer(txt, reply_markup=btn)
        await ChangeLang.next()


@dp.message_handler(state=ChangeLang.lang)
async def change_lang(msg: types.Message, state: FSMContext):
    if msg.text in ("🇺🇿 O'zbek tili", "🇷🇺 Русский язык", "🇬🇧 English"):
        if msg.text == "🇺🇿 O'zbek tili":
            db.update_user_lang(lang='uz', tg_id=msg.from_user.id)
        elif msg.text == "🇷🇺 Русский язык":
            db.update_user_lang(lang='ru', tg_id=msg.from_user.id)
        else:
            db.update_user_lang(lang='en', tg_id=msg.from_user.id)
        lang = db.select_user_lang(tg_id=msg.from_user.id)
        txt = msg_lang['success_lang'][lang[0]]
        if str(msg.from_user.id) in ADMINS:
            btn = get_main_menu_admin(lang[0])
        else:
            btn = get_main_menu(lang[0])
        await msg.answer(txt, reply_markup=btn)
        await state.finish()
    else:
        return
