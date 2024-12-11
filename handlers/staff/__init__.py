from aiogram import Router

from middlewares.user import UserMiddleware, StaffMiddleware

from .group import r as group_r
from .event import r as event_r
from .base import r as base_r

router = Router()
router.message.middleware(UserMiddleware())
router.message.middleware(StaffMiddleware())
router.callback_query.middleware(UserMiddleware())
router.callback_query.middleware(StaffMiddleware())
router.include_routers(base_r, group_r, event_r)
