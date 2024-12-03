from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from tortoise.exceptions import DoesNotExist

from callbacks.staff.group import GroupCallback
from database.models.user import User
from database.models.group import Group
from services.base import field, not_found, permission_denied
from keyboards.staff.group import group_keyboard


def _empty_txt() -> str:
    return "У тебя нет групп, чего ты хочешь? 0_0"


async def groups_empty(msg: Message, edit: bool = False):
    if edit:
        return await msg.edit_text(_empty_txt(), reply_markup=None)
    else:
        return await msg.answer(_empty_txt(), reply_markup=None)


async def groups_list(msg: Message, user: User, edit: bool = False):
    builder = InlineKeyboardBuilder()

    for group in user.owned_groups:
        builder.button(text=group.name,
                       callback_data=GroupCallback(id=group.id))

    builder.adjust(1)
    if edit:
        return await msg.edit_text("Выбери группу из списка ниже:", reply_markup=builder.as_markup())
    else:
        return await msg.answer("Выбери группу из списка ниже:", reply_markup=builder.as_markup())


async def groups_404(msg: Message, gid: int):
    callback_data = f"{GroupCallback.__prefix__}:{gid}"
    markup = InlineKeyboardMarkup(inline_keyboard=[[el for el in line if el.callback_data != callback_data]
                                                   for line in msg.reply_markup])
    if any(markup):
        return await msg.edit_reply_markup(reply_markup=markup)
    else:
        return await msg.edit_text(text=_empty_txt(), reply_markup=None)


async def group_index(msg: Message, group: Group):
    await msg.edit_text(
        f"Редактирование группы #{group.id}\n"
        f"\n"
        f"<b>Название</b>: {group.name}\n"
        f"<b>Описание</b>: {field(group.desc)}",
        reply_markup=group_keyboard(group.id)
    )


async def create_group(msg: Message, name: str, user: User):
    g = await Group.create(owner=user, name=name)
    return await msg.answer(f"Я сделаль: создано Группа #{g.id}: {g.name} ")


async def my_groups(msg: Message, user: User, edit: bool = False):
    await user.fetch_related("owned_groups")

    if len(user.owned_groups):
        return await groups_list(msg, user, edit=edit)
    return await groups_empty(msg, edit=edit)


async def open_group(callback: CallbackQuery, callback_data: GroupCallback, user: User) -> Group | None:
    try:
        group = await Group.get(id=callback_data.id)
        owner = await group.owner
        assert owner.id == user.id
        return group

    except DoesNotExist:
        await not_found(callback, f"Группа #{callback_data.id}")
        await groups_list(callback.message, user, True)

    except AssertionError:
        await permission_denied(callback)
