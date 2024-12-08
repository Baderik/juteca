from aiogram.filters.callback_data import CallbackData


class EventCallback(CallbackData, prefix="staffEvent"):
    id: int


class EventEditCallback(CallbackData, prefix="staffEventEdit"):
    id: int
    value: str


class EventGroupCallback(CallbackData, prefix="staffEventGroup"):
    id: int
    group_id: int
    is_used: bool
