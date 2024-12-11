from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "blocked" INT NOT NULL  DEFAULT 0;
        ALTER TABLE "events" ADD "desc" TEXT NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "blocked";
        ALTER TABLE "events" DROP COLUMN "desc";"""
