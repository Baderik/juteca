from aiogram.filters.callback_data import CallbackData


class GroupCallback(CallbackData, prefix="defaultGroup"):
    id: int


class GroupPageCallback(CallbackData, prefix="defaultGroupPage"):
    search: str
    page: int
