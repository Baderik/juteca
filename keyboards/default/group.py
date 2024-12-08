from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.default.group import GroupCallback, GroupPageCallback
from database.models import Group, User


def group_btn_text(el: Group, user: User) -> str:
    if el in user.owned_groups:
        return f"👾 {el.name}"

    if el in user.groups:
        return f"✔️ {el.name}"
    return el.name


def group_page_keyboard(user: User, data: list[Group], search: str, before: int, after: int):
    builder = InlineKeyboardBuilder()
    if before:
        builder.button(text="« Предыдущие", callback_data=GroupPageCallback(search=search, page=before))

    for group in data:
        builder.button(
            text=group_btn_text(group, user),
            callback_data=GroupCallback(id=group.id)
        )

    if after:
        builder.button(text="Следующие »", callback_data=GroupPageCallback(search=search, page=after))
    builder.adjust(1)
    return builder.as_markup()

