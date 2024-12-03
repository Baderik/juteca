from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from tortoise.exceptions import DoesNotExist

from callbacks.staff.group import GroupCallback, GroupEditCallback
from database.models.user import User
from database.models.group import Group
from services.staff.group import groups_list, groups_empty, group_index
from services.base import not_found, permission_denied
from dialogs.staff.group import CreateGroup

r = Router()


async def create_group(msg: Message, name: str, user: User):
    g = await Group.create(owner=user, name=name)
    return await msg.answer(f"Я сделаль: создано Группа #{g.id}: {g.name} ")


@r.message(Command('newGroup'))
async def h_new_group(msg: Message, user: User, command: CommandObject, state: FSMContext):
    if command.args:
        return await create_group(msg, command.args, user)

    await state.set_state(CreateGroup.choosing_name)

    return await msg.answer(f"Теперь придумай <u>название группы</u>. "
                            f"Отправь его следующим сообщением, либо набери /cancel для отмены")


@r.message(CreateGroup.choosing_name)
async def h_new_group(msg: Message, user: User, state: FSMContext):
    await create_group(msg, msg.text, user)
    await state.clear()


async def my_groups(msg: Message, user: User, edit: bool = False):
    await user.fetch_related("owned_groups")

    if len(user.owned_groups):
        return await groups_list(msg, user, edit=edit)
    return await groups_empty(msg, edit=edit)


@r.message(Command('myGroups'))
async def h_my_groups_command(msg: Message, user: User):
    await my_groups(msg, user)


@r.callback_query(F.data == "myGroups")
async def h_my_groups_callback(callback: CallbackQuery, user: User):
    await my_groups(callback.message, user, True)
    await callback.answer()


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


@r.callback_query(GroupCallback.filter())
async def h_group(callback: CallbackQuery, callback_data: GroupCallback, user: User):
    group = await open_group(callback, callback_data, user)
    await group_index(callback.message, group)


@r.callback_query(GroupEditCallback.filter())
async def h_group_edit(callback: CallbackQuery, callback_data: GroupEditCallback, user: User):
    await open_group(callback, GroupCallback(id=callback_data.id), user)

    await callback.answer("Прости🙏🏻, но это пока не работает)")
