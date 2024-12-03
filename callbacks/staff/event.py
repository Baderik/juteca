from aiogram.filters.callback_data import CallbackData


class EventCallback(CallbackData, prefix="event"):
    id: int


class EventEditCallback(CallbackData, prefix="event_edit"):
    id: int
    value: str
