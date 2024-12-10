from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.staff.upgrade import UpgradeCallback


def answer_upgrade_keyboard(rid: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Одобрено",
        callback_data=UpgradeCallback(id=rid, approved=True),
    )
    builder.button(
        text="Отклонено",
        callback_data=UpgradeCallback(id=rid, approved=False),
    )
    builder.adjust(2)
    return builder.as_markup()
