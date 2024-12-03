from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from callbacks.staff.group import GroupCallback, GroupEditCallback
from database.models.user import User
from services.staff.group import group_index, create_group, my_groups, open_group

from dialogs.staff.group import CreateGroup

r = Router()


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


@r.message(Command('myGroups'))
async def h_my_groups_command(msg: Message, user: User):
    await my_groups(msg, user)


@r.callback_query(F.data == "myGroups")
async def h_my_groups_callback(callback: CallbackQuery, user: User):
    await my_groups(callback.message, user, True)
    await callback.answer()


@r.callback_query(GroupCallback.filter())
async def h_group(callback: CallbackQuery, callback_data: GroupCallback, user: User):
    group = await open_group(callback, callback_data, user)
    await group_index(callback.message, group)


@r.callback_query(GroupEditCallback.filter())
async def h_group_edit(callback: CallbackQuery, callback_data: GroupEditCallback, user: User):
    await open_group(callback, GroupCallback(id=callback_data.id), user)

    await callback.answer("Прости🙏🏻, но это пока не работает)")
