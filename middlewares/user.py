from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database.models.user import User
from config import config


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user = data["event_from_user"]
        context = data["event_context"]

        data['user'] = await self.get_userdata(user.id, user.username, context.chat.id)

        if not data['user'].is_active:
            await event.answer(
                "Привет Незнакомец -_-...\n"
                "Перед началом работы нам нужно познакомиться. "
                "Для этого напиши мне что-нибудь в личные сообщения, например: /start")
            return

        if data['user'].telegram_id in config.super_users:
            return await handler(event, data)

        await event.answer("Доступ закрыт")

    @staticmethod
    async def get_userdata(telegram_id: int, username: str, chat_id: int) -> User:
        user, _ = await User.get_or_create(telegram_id=telegram_id)
        await user.update_chat_data(chat_id=chat_id, username=username)
        return user


class StaffMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        await super().__call__(handler, event, data)

        if not data['user'].is_staff:
            await event.answer(
                "Это доступно только работникам, не везет тебе =)")
            return
        return await handler(event, data)
