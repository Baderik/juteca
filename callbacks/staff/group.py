from aiogram.filters.callback_data import CallbackData


class GroupCallback(CallbackData, prefix="staffGroup"):
    id: int


class GroupEditCallback(CallbackData, prefix="staffGroupEdit"):
    id: int
    value: str
