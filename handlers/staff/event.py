from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from callbacks.staff.event import EventCallback, EventEditCallback
from callbacks.base import YesNoCallback
from database.models.user import User
from database.enums import short_weekday, WeekDay
from dialogs.staff.event import EditEvent
from services.staff.event import (my_events, msg_choosing_weekday, msg_choosing_title, msg_choosing_daytime,
                                  create_event, open_event, msg_set_event, wait_title, wait_delete, update_event)

r = Router()


@r.message(Command('myEvents'))
async def h_my_events_command(msg: Message, user: User):
    await my_events(msg, user)


@r.callback_query(F.data == "myEvents")
async def h_my_events_callback(callback: CallbackQuery, user: User):
    await my_events(callback.message, user, True)
    await callback.answer()


@r.message(Command('newEvent'))
async def h_new_group(msg: Message, command: CommandObject, state: FSMContext):
    if command.args:
        await state.set_state(EditEvent.choosing_weekday)
        await state.update_data({"title": command.args})
        await msg_choosing_weekday(msg)
    else:
        await state.set_state(EditEvent.choosing_title)
        await msg_choosing_title(msg)


@r.message(EditEvent.choosing_title)
async def h_create_title(msg: Message, user: User, state: FSMContext):
    data = await state.get_data()
    if eid := data.get("eid"):
        return await update_event(msg, eid, user, title=msg.text)
    await state.set_state(EditEvent.choosing_weekday)
    await state.update_data({"title": msg.text})
    await msg_choosing_weekday(msg)


@r.message(EditEvent.choosing_weekday, F.text.in_(short_weekday))
async def h_create_weekday(msg: Message, state: FSMContext):

    await state.set_state(EditEvent.choosing_daytime)
    await state.update_data({"week_day": WeekDay.by_day(msg.text)})
    await msg_choosing_daytime(msg)


@r.message(EditEvent.choosing_weekday)
async def h_create_weekday(msg: Message):
    await msg.answer("Не делай так, не делай.... Пожалуйста выбери день, нажав на одну из кнопок.")


@r.message(EditEvent.choosing_daytime)
async def s_time(msg: Message, user: User, state: FSMContext):
    hour, *minutes = msg.text.split(":")
    txt = "В формате {часы}:{минуты}, пожалуйста..."
    if len(minutes) != 1 or (not (hour.isdigit() and 0 <= int(hour) < 24)):
        return await msg.answer(text=txt)
    minutes = minutes[0]
    if not (minutes.isdigit() and 0 <= int(minutes) < 60):
        return await msg.answer(text=txt)
    await state.update_data(day_time=f"{hour:0>2}:{minutes:0>2}")
    data = await state.get_data()
    await create_event(msg, user, **data)


@r.callback_query(EventCallback.filter())
async def h_event(callback: CallbackQuery, callback_data: EventCallback, user: User):
    event = await open_event(callback, callback_data.id, user)
    await msg_set_event(callback.message, event)


@r.callback_query(EventEditCallback.filter())
async def h_event_edit(callback: CallbackQuery, callback_data: EventEditCallback, state: FSMContext, user: User):
    event = await open_event(callback, callback_data.id, user)

    match callback_data.value:
        case "title":
            await wait_title(callback.message, state)
        # case "weekday":
        #     await wait_description(callback.message, state)
        # case "daytime":
        #     await wait_description(callback.message, state)
        case "delete":
            await wait_delete(callback.message, event, state)
        case _:
            await callback.answer("Прости🙏🏻, но это пока не работает)")

    await state.update_data(eid=event.id)


@r.callback_query(EditEvent.try_delete and YesNoCallback.filter())
async def h_event_delete(callback: CallbackQuery, callback_data: YesNoCallback, user: User):
    event = await open_event(callback, callback_data.id, user)
    if callback_data.is_yes:
        await callback.message.answer(f"Мои поздравления, мероприятие {event.head} более не существует")
        await event.delete()
        await my_events(callback.message, user, True)
        await callback.answer()

    else:
        await msg_set_event(callback.message, event)
