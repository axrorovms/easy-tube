from aiogram import types 
from aiogram.dispatcher import FSMContext
from loader import dp, db 
from data.translate import msg_lang
from states.youtube_states import Youtube

@dp.message_handler(lambda x: x.text in ("Download video 📥", "Video yuklash 📥", "Скачать видео 📥")) 
async def send_link_to_download(msg: types.Message):
    lang = db.select_user_lang(tg_id=msg.from_user.id)
    txt = msg_lang["send_link"][lang[0]]
    await msg.answer(txt)
    await Youtube.first()

@dp.message_handler(state=Youtube.link)
async def download_you_tube_video(msg: types.Message, state=FSMContext):
    lang = db.select_user_lang(tg_id=msg.from_user.id)
    from googleapiclient.discovery import build
from pytube import YouTube

# Set your API key
api_key = 'YOUR_API_KEY'


youtube = build('youtube', 'v3', developerKey=api_key)


channel_id = 'UC_x5XG1OV2P6uZZ5FSM9Ttw'  # Example channel ID (Google Developers)

playlist_response = youtube.channels().list(
    part='contentDetails',
    id=channel_id
).execute()
playlist_id = playlist_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']


playlist_items = youtube.playlistItems().list(
    part='snippet',
    playlistId=playlist_id,
    maxResults=5
).execute()

for item in playlist_items['items']:
    video_title = item['snippet']['title']
    video_id = item['snippet']['resourceId']['videoId']
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    print(f'Title: {video_title}\nURL: {video_url}\n')







