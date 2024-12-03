from tortoise import Tortoise

# from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB

# TORTOISE_ORM = {
#     "connections": {
#         "default": f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
#     },
#     "apps": {
#         "models": {
#             "models": ["bot.models", "aerich.models"],
#             "default_connection": "default",
#         },
#     },
# }

ORM_CONFIG = {
    "db_url": "sqlite://db.sqlite3",
    "modules": {'models': ["database.models"]},
}


async def init_db():
    await Tortoise.init(**ORM_CONFIG)
    await Tortoise.generate_schemas()
