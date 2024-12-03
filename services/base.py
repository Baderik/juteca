from aiogram.types import CallbackQuery, Message


async def not_found(callback: CallbackQuery, txt: str):
    return await callback.answer(f"Ой-ой, {txt} не найдено (?_?)", alert=True)


async def permission_denied(t_obj: CallbackQuery | Message):
    txt: str = "Нет, нет, сюда тебе нельзя"
    match type(t_obj):
        case CallbackQuery():
            return await t_obj.answer(txt, alert=True)
        case Message():
            return await t_obj.answer(txt)


def field(txt: str) -> str:
    if txt:
        return txt
    else:
        return "🚫"
