from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from config import config
from database.models import User, UpgradeRequest
from services.staff.upgrade import send_requests_superusers

r = Router()


@r.message(Command("staff"))
async def h_staff(msg: Message, state: FSMContext, user: User, bot: Bot):
    await state.clear()
    if user.is_staff:
        await msg.answer("ТЫ!!!! УЖЕ!!!! СОТРУДНИК!!!!", reply_markup=ReplyKeyboardRemove())
        return

    if user.telegram_id in config.super_users:
        if user.is_staff:
            await msg.answer("Cэмпай (^•^)... не делай так", reply_markup=ReplyKeyboardRemove())
            return
        user.is_staff = True
        await user.save()
        await msg.answer("Я вспомнил тебя, сэмпай ≽^•⩊•^≼", reply_markup=ReplyKeyboardRemove())
        return

    req = await UpgradeRequest.get_or_none(sender=user, finished=False)

    if req:
        await msg.answer("Твой предыдущий запрос еще не обработали, поэтому жди", reply_markup=ReplyKeyboardRemove())
        return

    upgrade = await UpgradeRequest.create(sender=user)
    await send_requests_superusers(bot, upgrade)

    await msg.answer("Заявку отправил, теперь жди", reply_markup=ReplyKeyboardRemove())
