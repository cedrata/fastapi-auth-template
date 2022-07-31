from typing import Final

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.db.collections import user

# TODO: Move to config file.
# TODO: Handle correctly secrets.
_DATABASE_USERNAME: Final[str] = "admin"
_DATABASE_PASSOWRD: Final[str] = "admin"
_DATABASE_HOST: Final[str] = "localhost"
_DATABASE_PORT: Final[str] = "27017"
_DATABASE_NAME: Final[str] = "fastapi_auth_template"

_CONNECTION_STRING = f"mongodb://{_DATABASE_USERNAME}:{_DATABASE_PASSOWRD}@{_DATABASE_HOST}:{_DATABASE_PORT}/{_DATABASE_NAME}"


async def build_client() -> None:
    client = AsyncIOMotorClient(_CONNECTION_STRING)
    await init_beanie(client.fastapi_auth_template, document_models=[user.User])
