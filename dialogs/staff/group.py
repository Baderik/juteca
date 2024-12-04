from aiogram.fsm.state import State, StatesGroup


class EditGroup(StatesGroup):
    choosing_name = State()
    choosing_description = State()
    try_delete = State()
