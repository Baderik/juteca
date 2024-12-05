from aiogram.fsm.state import State, StatesGroup


class EditEvent(StatesGroup):
    choosing_title = State()
    choosing_weekday = State()
    choosing_daytime = State()
    try_delete = State()
    choosing_groups = State()
