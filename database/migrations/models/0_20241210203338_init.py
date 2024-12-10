from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "telegram_id" INT NOT NULL,
    "chat_id" INT,
    "username" VARCHAR(32)
);
CREATE TABLE IF NOT EXISTS "groups" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(256) NOT NULL,
    "desc" TEXT NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "events" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "title" VARCHAR(256) NOT NULL,
    "week_day" SMALLINT NOT NULL  /* monday: 0\ntuesday: 1\nwednesday: 2\nthursday: 3\nfriday: 4\nsaturday: 5\nsunday: 6 */,
    "time" TIME NOT NULL,
    "is_active" INT NOT NULL  DEFAULT 1,
    "author_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "groups_user" (
    "groups_id" INT NOT NULL REFERENCES "groups" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_groups_user_groups__511810" ON "groups_user" ("groups_id", "user_id");
CREATE TABLE IF NOT EXISTS "events_groups" (
    "events_id" INT NOT NULL REFERENCES "events" ("id") ON DELETE CASCADE,
    "group_id" INT NOT NULL REFERENCES "groups" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_events_grou_events__f97ae3" ON "events_groups" ("events_id", "group_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
