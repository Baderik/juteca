from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.staff.group import GroupEditCallback


def group_keyboard(gid):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Изменить Название",
        callback_data=GroupEditCallback(id=gid, value="name"),
    )
    builder.button(
        text="Изменить Описание",
        callback_data=GroupEditCallback(id=gid, value="desc"),
    )
    builder.button(
        text="Удалить Группу",
        callback_data=GroupEditCallback(id=gid, value="delete"),
    )
    builder.button(
        text="« К списку групп",
        callback_data="myGroups"
    )
    builder.adjust(2)
    return builder.as_markup()
