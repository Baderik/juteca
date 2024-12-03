from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tortoise.exceptions import DoesNotExist

from callbacks.staff.event import EventCallback
from database.models.user import User
from database.models.event import Event
from services.base import not_found, permission_denied
from keyboards.staff.event import weekday_markup, event_keyboard


def _empty_txt() -> str:
    return "У тебя нет мероприятий, поэтому здесь ничего не найдешь 0_0"


async def events_empty(msg: Message, edit: bool = False):
    if edit:
        return await msg.edit_text(_empty_txt(), reply_markup=None)
    else:
        return await msg.answer(_empty_txt(), reply_markup=None)


async def events_list(msg: Message, user: User, edit: bool = False):
    builder = InlineKeyboardBuilder()

    for event in user.created_events:
        builder.button(text=event.title,
                       callback_data=EventCallback(id=event.id))

    builder.adjust(1)
    if edit:
        return await msg.edit_text("Выбери мероприятие из списка ниже:", reply_markup=builder.as_markup())
    else:
        return await msg.answer("Выбери мероприятие из списка ниже:", reply_markup=builder.as_markup())


async def event_index(msg: Message, event: Event):
    await msg.edit_text(
        f"Редактирование Мероприятия #{event.id}\n"
        f"\n"
        f"<b>Название</b>: {event.title}\n"
        f"<b>Расписание</b>: {event.week_day.title} в {event.time}",
        reply_markup=event_keyboard(event.id)
    )


async def create_event(msg: Message, user: User, title: str, week_day, day_time):
    g = await Event.create(author=user, title=title, week_day=week_day, time=day_time)
    return await msg.answer(f"Я сделаль: создано Мероприятие #{g.id}: {g.title} ")


async def my_events(msg: Message, user: User, edit: bool = False):
    await user.fetch_related("created_events")

    if len(user.created_events):
        return await events_list(msg, user, edit=edit)
    return await events_empty(msg, edit=edit)


async def msg_choosing_title(msg: Message):
    return await msg.answer(f"Теперь придумай <u>название мероприятия</u>. "
                            f"Отправь его следующим сообщением, либо набери /cancel для отмены")


async def msg_choosing_weekday(msg: Message):
    return await msg.answer(f"Выбери <u>день недели</u> занятий", reply_markup=weekday_markup)


async def msg_choosing_daytime(msg: Message):
    return await msg.answer("Отправь <u>время занятия</u> в формате {часы}:{минуты}")


async def open_event(callback: CallbackQuery, callback_data: EventCallback, user: User) -> Event | None:
    try:
        event = await Event.get(id=callback_data.id)
        author = await event.author
        assert author.id == user.id
        return event

    except DoesNotExist:
        await not_found(callback, f"Мероприятие #{callback_data.id}")
        await events_list(callback.message, user, True)

    except AssertionError:
        await permission_denied(callback)
