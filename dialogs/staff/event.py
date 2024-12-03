from aiogram.fsm.state import State, StatesGroup


class CreateEvent(StatesGroup):
    choosing_title = State()
    choosing_weekday = State()
    choosing_daytime = State()

