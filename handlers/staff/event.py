from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from callbacks.staff.event import EventCallback, EventEditCallback
from database.models.user import User
from database.enums import weekday_str, WeekDay
from dialogs.staff.event import CreateEvent
from services.staff.event import my_events, msg_choosing_weekday, msg_choosing_title, msg_choosing_daytime, create_event, open_event, event_index

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
        print(command.args)
        await state.set_state(CreateEvent.choosing_weekday)
        await state.update_data({"title": command.args})
        await msg_choosing_weekday(msg)
    else:
        await state.set_state(CreateEvent.choosing_title)
        await msg_choosing_title(msg)


@r.message(CreateEvent.choosing_title)
async def h_create_title(msg: Message, state: FSMContext):
    await state.set_state(CreateEvent.choosing_weekday)
    await state.update_data({"title": msg.text})
    await msg_choosing_weekday(msg)


@r.message(CreateEvent.choosing_weekday, F.text.in_(weekday_str))
async def h_create_weekday(msg: Message, state: FSMContext):
    await state.set_state(CreateEvent.choosing_daytime)
    await state.update_data({"week_day": WeekDay.by_day(msg.text)})
    await msg_choosing_daytime(msg)


@r.message(CreateEvent.choosing_weekday)
async def h_create_weekday(msg: Message):
    await msg.answer("Не делай так, не делай.... Пожалуйста выбери день, нажав на одну из кнопок.")


@r.message(CreateEvent.choosing_daytime)
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
    event = await open_event(callback, callback_data, user)
    await event_index(callback.message, event)


@r.callback_query(EventEditCallback.filter())
async def h_group_edit(callback: CallbackQuery, callback_data: EventEditCallback, user: User):
    await open_event(callback, EventCallback(id=callback_data.id), user)

    await callback.answer("Прости🙏🏻, но это пока не работает)")
