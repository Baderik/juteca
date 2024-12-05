from aiogram.filters.callback_data import CallbackData


class EventCallback(CallbackData, prefix="event"):
    id: int


class EventEditCallback(CallbackData, prefix="event_edit"):
    id: int
    value: str


class EventGroupCallback(CallbackData, prefix="event_group"):
    id: int
    group_id: int
    is_used: bool
