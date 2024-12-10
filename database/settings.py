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
    "connections": {
            "default": "sqlite://db.sqlite3"
            },
    "apps": {
            "models": {
                "models": ["database.models", "aerich.models"],
                "default_connection": "default",
            },
        }
}
