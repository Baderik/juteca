from aiogram.fsm.state import State, StatesGroup


class CreateGroup(StatesGroup):
    choosing_name = State()
