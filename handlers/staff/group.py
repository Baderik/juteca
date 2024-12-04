from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from callbacks.staff.group import GroupCallback, GroupEditCallback
from callbacks.base import YesNoCallback
from database.models.user import User
from services.staff.group import msg_set_group, create_group, my_groups, open_group, wait_name, update_group, wait_description, wait_delete

from dialogs.staff.group import EditGroup

r = Router()


@r.message(Command('newGroup'))
async def h_new_group(msg: Message, user: User, command: CommandObject, state: FSMContext):
    await state.clear()

    if command.args:
        return await create_group(msg, command.args, user)

    await wait_name(msg, state)


@r.message(EditGroup.choosing_name)
async def h_group_name(msg: Message, user: User, state: FSMContext):
    data = await state.get_data()
    if gid := data.get("gid"):
        await update_group(msg, gid, user, name=msg.text)
    else:
        await create_group(msg, msg.text, user)
    await state.clear()


@r.message(EditGroup.choosing_description)
async def h_group_desc(msg: Message, user: User, state: FSMContext):
    data = await state.get_data()
    if gid := data.get("gid"):
        await update_group(msg, gid, user, desc=msg.text)
    await state.clear()


@r.message(Command('myGroups'))
async def h_my_groups_command(msg: Message, user: User):
    await my_groups(msg, user)


@r.callback_query(F.data == "myGroups")
async def h_my_groups_callback(callback: CallbackQuery, user: User):
    await my_groups(callback.message, user, True)
    await callback.answer()


@r.callback_query(GroupCallback.filter())
async def h_group(callback: CallbackQuery, callback_data: GroupCallback, user: User):
    group = await open_group(callback, callback_data.id, user)
    await msg_set_group(callback.message, group)


@r.callback_query(GroupEditCallback.filter())
async def h_group_edit(callback: CallbackQuery, callback_data: GroupEditCallback, state: FSMContext, user: User):
    group = await open_group(callback, callback_data.id, user)

    match callback_data.value:
        case "name":
            await wait_name(callback.message, state)
        case "desc":
            await wait_description(callback.message, state)
        case "delete":
            await wait_delete(callback.message, group, state)
        case _:
            await callback.answer("Прости🙏🏻, но это пока не работает)")

    await state.update_data(gid=group.id)


@r.callback_query(EditGroup.try_delete and YesNoCallback.filter())
async def h_group_delete(callback: CallbackQuery, callback_data: YesNoCallback, user: User):
    group = await open_group(callback, callback_data.id, user)
    if callback_data.is_yes:
        await callback.message.answer(f"Мои поздравления, группы {group.head} более не существует")
        await group.delete()
        await my_groups(callback.message, user, True)
        await callback.answer()

    else:
        await msg_set_group(callback.message, group)
