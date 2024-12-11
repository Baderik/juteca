from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from services.default.base import help_text

r = Router()


@r.message(Command("start"))
async def h_start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Приветь, котя", reply_markup=ReplyKeyboardRemove())


@r.message(Command("cancel"))
async def h_cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Всё что было - забыто, всё что будет... - будет", reply_markup=ReplyKeyboardRemove())


@r.message(Command("help"))
async def h_cancel(msg: Message):
    await msg.answer(help_text())
