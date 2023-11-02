import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
PASSWORD = os.getenv("DB_PASSWD", "123456")
DB_USER = os.getenv("DB_USER", "chat")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "chat")

DB_BASE_URL = f"postgres://{DB_USER}:{PASSWORD}@{DB_HOST}:{DB_PORT}"


TORTOISE_ORM: dict[str, Any] = {
    "connections": {"default": f"{DB_BASE_URL}/{DB_NAME}"},
    "apps": {
        "models": {
            "models": ["aerich.models", "src.models"],
            "default_connection": "default",
        }
    },
}
