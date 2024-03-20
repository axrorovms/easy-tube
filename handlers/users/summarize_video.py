from aiogram import types 
from aiogram.dispatcher import FSMContext
from youtube_transcript_api import YouTubeTranscriptApi as yta
from loader import dp, db  
from data.translate import msg_lang
from data.config import ADMINS
from states.youtube_states import YoutubeSummarize
from keyboards.default.cancel import cancel_btn 
from keyboards.default.start_buttons import get_main_menu, get_main_menu_admin
from utils.validation import valid_video_url
from utils.ask_gpt import gpt
from utils.own_functions import format_text
import re

VIDEO_ID_PATTERN = re.compile(r"(?<=v=)[\w-]+")

@dp.message_handler(lambda x: x.text in ("Videoni umumlashtirish 📝", "Обобщить видео 📝", "Summarize video 📝")) 
async def send_link_to_download(msg: types.Message):
    lang = db.select_user_lang(tg_id=msg.from_user.id)
    txt = msg_lang["send_link"][lang[0]]
    btn = cancel_btn(lang[0])
    await msg.answer(txt, reply_markup=btn)
    await YoutubeSummarize.first()

@dp.message_handler(state=YoutubeSummarize.link)
async def summarize_you_tube_video(msg: types.Message, state=FSMContext):
    await msg.answer_sticker(sticker='CAACAgQAAxkBAAIezWX5K79DN5HtKb2VOERSwG7iPHIjAAIBBAACWD7TBSQU5R7Y3SP8NAQ')
    lang = db.select_user_lang(tg_id=msg.from_user.id)
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
    match = VIDEO_ID_PATTERN.search(msg.text)
    vid_id = match.group(0)
    data = yta.get_transcript(vid_id)
    transcript_segments = []
    for value in data:
        for key, val in value.items():
            if key == 'text':
               transcript_segments.append(val)
    result = ' '.join(transcript_segments)
    await msg.answer(msg_lang['generating_ans'][lang[0]])
    await msg.answer(format_text(gpt(result)), reply_markup=btn)
    await state.finish()


   
