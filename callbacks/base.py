from aiogram.filters.callback_data import CallbackData


class YesNoCallback(CallbackData, prefix="yes_no"):
    id: int
    is_yes: bool
