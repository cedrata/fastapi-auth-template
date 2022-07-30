import json

import pytest
from httpx import AsyncClient
from tests import build_db_client, fastapi_app


@pytest.mark.asyncio
async def test_login():
    await build_db_client()
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        response = await ac.post(
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
    assert response.status_code == 200
    response_json: dict = json.loads(response.text)
    assert "access_token" in response_json.keys()
    assert "refresh_token" in response_json.keys()
    assert "token_type" in response_json.keys()


@pytest.mark.asyncio
async def test_bad_username_login():
    await build_db_client()
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "grant_type": "",
                "username": "admon",
                "password": "admin",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_bad_password_login():
    await build_db_client()
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "grant_type": "",
                "username": "admin",
                "password": "admon",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )
    assert response.status_code == 401
