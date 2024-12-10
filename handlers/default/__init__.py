from aiogram import Router

from middlewares.user import UserMiddleware

from .base import r as base_r
from .group import r as group_r
from .timetable import r as timetable_r
from .upgrade import r as upgrade_r


router = Router()
router.message.middleware(UserMiddleware())
router.callback_query.middleware(UserMiddleware())
router.include_routers(base_r, group_r, timetable_r, upgrade_r)
