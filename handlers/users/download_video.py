from aiogram import types
from aiogram.dispatcher import FSMContext
from pytube import YouTube
from data.translate import msg_lang
from data.config import ADMINS
from keyboards.default.cancel import cancel_btn
from keyboards.default.start_buttons import get_main_menu, get_main_menu_admin
from states.youtube_states import YoutubeDownload
from utils.validation import valid_video_url
from loader import dp, db, bot
import yt_dlp

@dp.message_handler(lambda x: x.text in ("Download video 📥", "Video yuklash 📥", "Скачать видео 📥"))
async def download_video(msg: types.Message):
    lang = db.select_user_lang(tg_id=msg.from_user.id)
    txt = msg_lang["send_link"][lang[0]]
    btn = cancel_btn(lang[0])
    await msg.answer(txt, reply_markup=btn)
    await YoutubeDownload.first()

@dp.message_handler(state=YoutubeDownload.link)
async def summarize_you_tube_video(msg: types.Message, state=FSMContext):
    lang = db.select_user_lang(tg_id=msg.from_user.id)
    await msg.answer_sticker(sticker='CAACAgQAAxkBAAIezWX5K79DN5HtKb2VOERSwG7iPHIjAAIBBAACWD7TBSQU5R7Y3SP8NAQ')
    if str(msg.from_user.id) in ADMINS:
        btn = get_main_menu_admin(lang[0])
    else:
        btn = get_main_menu(lanh[0])
    if msg.text in ("Отмена", "Bekor qilish", "Cancel"):
        if str(msg.from_user.id) in ADMINS:
            txt = msg_lang["main_menu"][lang[0]]
            await state.finish()
            await msg.answer(txt, reply_markup=btn)
            return
        txt = msg_lang["main_menu"][lang[0]]
        await msg.answer(txt, reply_markup=btn)
        await state.finish()
        return
    valid = valid_video_url(msg.text)
    if not valid:
        await msg.answer("please enter youtube video url") 
        return

    ydl = yt_dlp.YoutubeDL()

    info = ydl.extract_info(msg.text, download=True)
    outtmpl = ydl.params.get('outtmpl', '%(title)s.%(ext)s')
    filename = ydl.prepare_filename(info) if outtmpl else None
    await msg.answer('almost here')
    await bot.send_video(chat_id=msg.chat.id, video=open(filename, 'rb'), reply_markup=btn)
    await state.finish()
