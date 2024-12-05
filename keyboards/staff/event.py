from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from callbacks.staff.event import EventEditCallback, EventCallback, EventGroupCallback
from callbacks.base import YesNoCallback
from database.enums import WeekDay
from database.models.event import Event
from database.models.user import User


def event_keyboard(eid):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="изменить Название",
        callback_data=EventEditCallback(id=eid, value="title"),
    )
    builder.button(
        text="изменить День недели",
        callback_data=EventEditCallback(id=eid, value="weekday"),
    )
    builder.button(
        text="изменить Время занятия",
        callback_data=EventEditCallback(id=eid, value="daytime"),
    )
    builder.button(
        text="связанные Группы",
        callback_data=EventEditCallback(id=eid, value="groups"),
    )
    builder.button(
        text="удалить Мероприятие",
        callback_data=EventEditCallback(id=eid, value="delete"),
    )
    builder.button(
        text="« К списку мероприятий",
        callback_data="myEvents"
    )
    builder.adjust(2)
    return builder.as_markup()


weekday_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                     keyboard=[[KeyboardButton(text=day.short_title) for day in WeekDay]])


def delete_event_keyboard(eid):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Да, удали это мероприятие :(",
        callback_data=YesNoCallback(id=eid, is_yes=True),
    )
    builder.button(
        text="Неть, оставь",
        callback_data=YesNoCallback(id=eid, is_yes=False),
    )
    builder.button(
        text="« К мероприятию",
        callback_data=EventCallback(id=eid)
    )
    builder.adjust(1)
    return builder.as_markup()


def event_groups_keyboard(event: Event, user: User):
    builder = InlineKeyboardBuilder()
    for group in user.owned_groups:
        used = group in event.groups
        builder.button(
            text=("✅ " if used else "") + group.head,
            callback_data=EventGroupCallback(id=event.id, group_id=group.id, is_used=used)
        )
    builder.button(
        text="« К мероприятию",
        callback_data=EventCallback(id=event.id)
    )
    builder.adjust(1)
    return builder.as_markup()
