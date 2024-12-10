from aiogram import Bot

from database.models import User, UpgradeRequest
from keyboards.staff.upgrade import answer_upgrade_keyboard

from config import config


def upgrade_msg_data(upgrade: UpgradeRequest) -> dict:
    return {
        "text": f"Новая заявка на становление сотрудником\n"
                f"от {upgrade.sender.head}",
        "reply_markup": answer_upgrade_keyboard(upgrade.id)
    }


async def send_requests_superusers(bot: Bot, upgrade: UpgradeRequest) -> None:
    super_users = await User.filter(telegram_id__in=config.SUPER_USERS).all()
    msg = upgrade_msg_data(upgrade)
    for super_user in super_users:
        if super_user.chat_id:
            await bot.send_message(super_user.chat_id, **msg)
