from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

r = Router()


@r.message(Command("start"))
async def h_start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Приветствую, сэмпай ≽^•⩊•^≼")


@r.message(Command("cancel"))
async def h_cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Всё что было - забыто, всё что будет... - будет", reply_markup=ReplyKeyboardRemove())
