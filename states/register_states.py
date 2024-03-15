from aiogram.dispatcher.filters.state import StatesGroup, State


class ChooseLang(StatesGroup):
    lang = State()


class UpdateNum(StatesGroup):
    num = State()
