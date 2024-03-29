from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from data.translate import msg_lang
from states.register_states import ChooseLang
from keyboards.default.start_buttons import get_main_menu, get_main_menu_admin
from keyboards.inline.lang_buttons import langs
from keyboards.default.phone_num import phone_num_btn
from loader import dp, db
from data.config import ADMINS


@dp.message_handler(CommandStart(), state="*")
async def bot_start(msg: types.Message, state: FSMContext):
    await state.finish()
    lang = db.select_user_lang(tg_id=msg.from_user.id)
    if lang:
        if str(msg.from_user.id) in ADMINS:
            txt = msg_lang["greeting"][lang[0]].format(msg.from_user.first_name)
            btn = get_main_menu_admin(lang[0])
            await msg.answer(txt, reply_markup=btn)
            return
        txt = msg_lang["greeting"][lang[0]].format(msg.from_user.first_name)
        btn = get_main_menu(lang[0])
        await msg.answer(txt, reply_markup=btn)
    else:
        txt = (
            f"Salom {msg.from_user.first_name}! Easytube ga xush kelibsiz)\n\n"
            f"•~•~•~•~•~•~•~•~•~\n\n"
            f"Привет {msg.from_user.first_name}! Добро пожаловать в Easytube)\n\n"
            f"•~•~•~•~•~•~•~•~•~\n\n"
            f"Hi {msg.from_user.first_name}! Welcome to Easytube!"
            f"\n\n🇺🇿 Tilni tanlang\n🇷🇺 Выберите язык\n🇬🇧 Choose language "
        )
        await msg.answer(txt, reply_markup=langs)


@dp.callback_query_handler(lambda c: c.data.startswith("lang"))
async def choose_l(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[1]
    tg_id = call.from_user.id
    username = call.from_user.username
    fullname = call.from_user.full_name
    db.create_user(
        tg_id=tg_id,
        username=username,
        fullname=fullname,
        lang=lang
    )
    grt = msg_lang['greeting'][lang].format(call.from_user.first_name)
    if tg_id in ADMINS:
        await call.message.delete()
        await call.message.answer(grt, reply_markup=get_main_menu_admin(lang))
        await state.finish()
    else:
        await call.message.delete()
        await call.message.answer(grt, reply_markup=get_main_menu(lang))
        await state.finish()
