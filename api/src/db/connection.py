from os import environ
from typing import Final

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.db.collections import user

# TODO: Move to config file.
# TODO: Handle correctly secrets.
_DATABASE_USERNAME: Final[str] = environ["DB_USERNAME"]
_DATABASE_PASSOWRD: Final[str] = environ["DB_PASSWORD"]
_DATABASE_HOST: Final[str] = environ["DB_HOST"]
_DATABASE_PORT: Final[str] = environ["DB_PORT"]
_DATABASE_NAME: Final[str] = environ["DB_NAME"]

_CONNECTION_STRING = f"mongodb://{_DATABASE_USERNAME}:{_DATABASE_PASSOWRD}@{_DATABASE_HOST}:{_DATABASE_PORT}/{_DATABASE_NAME}"


async def build_client() -> None:
    client = AsyncIOMotorClient(_CONNECTION_STRING)
    await init_beanie(
        client[_DATABASE_NAME], document_models=[user.User], allow_index_dropping=True
    )
