from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime

from database.models.user import User
from database.models.event import Event
from database.enums import WeekDay


r = Router()


async def text_schedule(events: list[Event]):
    if not events:
        return "Пока что здесь пусто ^_^"
    return "\n".join(f"<b>{event.time.strftime("%H:%M")}</b> - {event.title}"
                     for event in sorted(events, key=lambda x: x.time))


async def day_schedule(user: User, day: WeekDay):
    await user.fetch_related("groups")
    events = await Event.filter(groups__in=user.groups, week_day=day)
    txt = f"Расписание на <i>{day.title}</i>"
    return f"{txt}\n\n{await text_schedule(events)}"


@r.message(Command("today"))
async def h_today(msg: Message, user: User):
    today = datetime.today().weekday()

    await msg.answer(await day_schedule(user, WeekDay(today)))


@r.message(Command("week"))
async def h_week(msg: Message, user: User):
    for day in range(7):
        await msg.answer(await day_schedule(user, WeekDay(day)))
