from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "is_staff" INT NOT NULL  DEFAULT 0;
        CREATE TABLE IF NOT EXISTS "upgraderequest" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "finished" INT NOT NULL  DEFAULT 0,
    "approved" INT,
    "moderator_id" INT REFERENCES "user" ("id") ON DELETE CASCADE,
    "sender_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "is_staff";
        DROP TABLE IF EXISTS "upgraderequest";"""
