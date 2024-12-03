from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from callbacks.staff.event import EventEditCallback
from database.enums import WeekDay


def event_keyboard(gid):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="изменить Название",
        callback_data=EventEditCallback(id=gid, value="title"),
    )
    builder.button(
        text="изменить День недели",
        callback_data=EventEditCallback(id=gid, value="weekday"),
    )
    builder.button(
        text="изменить Время занятия",
        callback_data=EventEditCallback(id=gid, value="daytime"),
    )
    builder.button(
        text="удалить Мероприятие",
        callback_data=EventEditCallback(id=gid, value="delete"),
    )
    builder.button(
        text="« К списку мероприятий",
        callback_data="myEvents"
    )
    builder.adjust(2)
    return builder.as_markup()


weekday_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                     keyboard=[[KeyboardButton(text=day.title) for day in WeekDay]])
