from aiogram import types
from data.translate import msg_lang
from loader import dp, db


@dp.message_handler(lambda x: x.text in ("Barcha userlar 👥", "Все юзеры 👥", "All users 👥"))
async def all_users(msg: types.Message):
    lang = db.select_user_lang(tg_id=msg.from_user.id)
    users = db.select_users()
    txt = f"{msg_lang['all_users'][lang[0]]} \n\n"
    for i in range(len(users)):
        if users[i][0] is None:
            txt += f'<b>{i+1}</b>. <b><i>{users[i][2]}</i></b> - {users[i][1]}\n'
        else:
            txt += f'<b>{i + 1}</b>. @{users[i][0]} - {users[i][1]}\n'
    await msg.answer(txt)
