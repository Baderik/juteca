from tortoise import Tortoise

from database.settings import ORM_CONFIG


async def init_db():
    await Tortoise.init(config=ORM_CONFIG)
    await Tortoise.generate_schemas()
