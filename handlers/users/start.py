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
            f"Assalomu Alaykum {msg.from_user.first_name}. Siz EasyTube botiga\n\n"
            f"•~•~•~•~•~•~•~•~•~\n\n"
            f"Привет {msg.from_user.first_name}. Вы посетили телеграм-бота, чтобы купить юань!"
            f"\n\n🇺🇿 Tilni tanlang\n🇷🇺 Выберите язык"
        )
        await msg.answer(txt, reply_markup=langs)


@dp.callback_query_handler(lambda c: c.data.startswith("lang"))
async def choose_l(call: types.CallbackQuery, state: FSMContext):
    print(111)
    await ChooseLang.first()
    lang = call.data.split("_")[1]
    await state.update_data(lang=lang)
    msg = msg_lang["request_phone"][lang]
    btn = phone_num_btn(lang)
    await call.message.delete()
    await call.message.answer(msg,reply_markup=btn)
