from aiogram import Router
from aiogram.filters import Command, CommandObject

from aiogram.types import Message, CallbackQuery

from database.models.user import User
from database.models.group import Group
from callbacks.default.group import GroupCallback, GroupPageCallback
from services.default.group import get_page
from keyboards.default.group import group_btn_text

r = Router()
LIMIT = 3


@r.message(Command('groups'))
async def h_groups_index(message: Message, user: User, command: CommandObject):
    response_data = await get_page(user, command.args if command.args else "", 1, LIMIT)
    await message.answer(**response_data)


@r.callback_query(GroupCallback.filter())
async def h_group(callback: CallbackQuery, callback_data: GroupCallback, user: User):
    if not (group := await Group.get_or_none(id=callback_data.id)):
        await callback.answer(f"Группа id={callback_data.id} не найдена (Не знаю, как ты это сделал, но ладно)")
        return

    await user.fetch_related('owned_groups')
    if group in user.owned_groups:
        await callback.answer(f"Ты не можешь избавиться от группы {group.head}")
        return

    await user.fetch_related('groups')
    if group in user.groups:
        await user.groups.remove(group)
        await user.save()
        await group.save()

        await callback.answer(f"Удалил тебя из группы {group.head}")

    else:
        await user.groups.add(group)
        await user.save()
        await group.save()

        await callback.answer(f"Добавил тебя в группу {group.head}")

    await user.fetch_related('groups')
    for line in callback.message.reply_markup.inline_keyboard:
        for btn in line:
            if GroupCallback.unpack(btn.callback_data) == callback_data:
                new_txt = group_btn_text(group, user)
                if new_txt == btn.text:
                    return
                btn.text = new_txt
                break
        else:
            continue
        break
    await callback.message.edit_reply_markup(reply_markup=callback.message.reply_markup)


@r.callback_query(GroupPageCallback.filter())
async def h_move_groups(callback: CallbackQuery, callback_data: GroupPageCallback, user: User):
    response_data = await get_page(user, callback_data.search, callback_data.page, LIMIT)
    await callback.message.edit_text(**response_data)
