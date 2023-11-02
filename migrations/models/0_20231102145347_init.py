from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "interactions" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "ai_model_name" VARCHAR(6) NOT NULL,
    "prompt" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "interactions"."ai_model_name" IS 'GPT3_5: gpt3_5\nGPT4: gpt4';
CREATE TABLE IF NOT EXISTS "messages" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "role" VARCHAR(6) NOT NULL  DEFAULT 'human',
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "interaction_id" UUID NOT NULL REFERENCES "interactions" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "messages"."role" IS 'SYSTEM: system\nAI: ai\nHUMAN: human';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
