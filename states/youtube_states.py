from aiogram.dispatcher.filters.state import StatesGroup, State

class YoutubeSummarize(StatesGroup):
    link = State()


class YoutubeDownload(StatesGroup):
    link = State()
