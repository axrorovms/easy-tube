from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType, Message

from data.config import ADMINS
from data.translate import msg_lang
from keyboards.default.start_buttons import get_main_menu_admin, get_main_menu
from loader import dp, db
from states.register_states import ChooseLang


@dp.message_handler(content_types=[ContentType.CONTACT], state=ChooseLang.lang)
async def register_user(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    lang = (await state.get_data())['lang']
    tg_id = message.from_user.id
    username = message.from_user.username
    db.create_user(
        tg_id=tg_id,
        username=username,
        phone=phone,
        lang=lang
    )
    grt = msg_lang['greeting'][lang].format(message.from_user.first_name)
    if tg_id in ADMINS:
        await message.answer(grt, reply_markup=get_main_menu_admin(lang))
    else:
        await message.answer(grt, reply_markup=get_main_menu(lang))
