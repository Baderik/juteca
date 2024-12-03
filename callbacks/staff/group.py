from aiogram.filters.callback_data import CallbackData


class GroupCallback(CallbackData, prefix="group"):
    id: int


class GroupEditCallback(CallbackData, prefix="group_edit"):
    id: int
    value: str
