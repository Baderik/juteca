from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.staff.base import help_text

r = Router()

@r.message(Command("help"))
async def h_cancel(msg: Message):
    await msg.answer(help_text())
