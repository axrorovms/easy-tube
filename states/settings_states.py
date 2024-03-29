from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeLang(StatesGroup):
    action = State()
    lang = State()

