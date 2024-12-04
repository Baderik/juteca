from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.staff.group import GroupEditCallback, GroupCallback
from callbacks.base import YesNoCallback


def group_keyboard(gid):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Расписание",
        callback_data=GroupEditCallback(id=gid, value="schedule"),
    )
    builder.button(
        text="изменить Название",
        callback_data=GroupEditCallback(id=gid, value="name"),
    )
    builder.button(
        text="изменить Описание",
        callback_data=GroupEditCallback(id=gid, value="desc"),
    )
    builder.button(
        text="удалить Группу",
        callback_data=GroupEditCallback(id=gid, value="delete"),
    )
    builder.button(
        text="связанные Мероприятия",
        callback_data=GroupEditCallback(id=gid, value="events"),
    )
    builder.button(
        text="« Список групп",
        callback_data="myGroups"
    )
    builder.adjust(2)
    return builder.as_markup()


def delete_group_keyboard(gid):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Да, удали эту группу :(",
        callback_data=YesNoCallback(id=gid, is_yes=True),
    )
    builder.button(
        text="Неть, оставь",
        callback_data=YesNoCallback(id=gid, is_yes=False),
    )
    builder.button(
        text="« К группе",
        callback_data=GroupCallback(id=gid)
    )
    builder.adjust(1)
    return builder.as_markup()
