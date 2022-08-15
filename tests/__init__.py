from json import loads as json_loads
from os import environ
from typing import Any, Final

import typesentry
from httpx import AsyncClient
from src.app import fastapi_app
from src.db.connection import build_client as build_db_client
from src.models.auth import AuthMessage

BASE_URL: Final[str] = "http://"

environ["SECRET_KEY"] = "test-secret-key"

_TC: Final[typesentry.Config] = typesentry.Config()
IS_TYPED: Final[Any] = _TC.is_type


async def admin_login() -> AuthMessage:
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        login_response = await ac.post(
            "/auth/login",
            data={
                "grant_type": "",
                "username": "admin",
                "password": "admin",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )
    return AuthMessage.parse_obj(json_loads(login_response.content))


async def user_login() -> AuthMessage:
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        login_response = await ac.post(
            "/auth/login",
            data={
                "grant_type": "",
                "username": "user",
                "password": "user",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )
    return AuthMessage.parse_obj(json_loads(login_response.content))
