from aiogram.filters.callback_data import CallbackData


class UpgradeCallback(CallbackData, prefix="staffUpgrade"):
    id: int
    approved: bool
