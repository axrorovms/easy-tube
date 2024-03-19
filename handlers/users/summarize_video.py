from aiogram import types 
from aiogram.dispatcher import FSMContext
from youtube_transcript_api import YouTubeTranscriptApi as yta
from loader import dp, db  
from data.translate import msg_lang
from states.youtube_states import Youtube
from utils.validation import valid_video_url
from utils.ask_gpt import gpt
from utils.own_functions import format_text
import re

VIDEO_ID_PATTERN = re.compile(r"(?<=v=)[\w-]+")

@dp.message_handler(lambda x: x.text in ("Download video 📥", "Video yuklash 📥", "Скачать видео 📥")) 
async def send_link_to_download(msg: types.Message):
    lang = db.select_user_lang(tg_id=msg.from_user.id)
    txt = msg_lang["send_link"][lang[0]]
    await msg.answer(txt)
    await Youtube.first()

@dp.message_handler(state=Youtube.link)
async def summarize_you_tube_video(msg: types.Message, state=FSMContext):
    lang = db.select_user_lang(tg_id=msg.from_user.id)
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
    await msg.answer(format_text(gpt(result)))
    await state.finish()

