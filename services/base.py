from aiogram.types import CallbackQuery, Message
from datetime import datetime


async def try_alert(t_obj: CallbackQuery | Message, txt: str):
    match type(t_obj):
        case CallbackQuery():
            return await t_obj.answer(txt, alert=True)
        case Message():
            return await t_obj.answer(txt)


async def not_found(t_obj: CallbackQuery | Message, txt: str):
    await try_alert(t_obj, f"Ой-ой, {txt} не найдено (?_?)")


async def permission_denied(t_obj: CallbackQuery | Message):
    await try_alert(t_obj, "Нет, нет, сюда тебе нельзя")


def field(txt: str) -> str:
    if txt:
        return txt
    else:
        return "🚫"


def field_related(f) -> str:
    if f:
        return "; ".join(map(lambda el: el.head, f))
    else:
        return "🚫"


def time_format(day_time: datetime.time) -> str:
    return day_time.strftime("%H:%M ")
