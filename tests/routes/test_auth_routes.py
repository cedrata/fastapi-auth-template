import json

import pytest
from httpx import AsyncClient
from src.routes.auth import login
from tests import build_db_client, fastapi_app, BASE_URL


@pytest.mark.asyncio
async def test_login():
    await build_db_client()
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
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
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
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
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
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


@pytest.mark.asyncio
async def test_refresh():
    await build_db_client()

    # Generate a valid token.
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

    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/auth/refresh",
            json={"refresh_token": json.loads(login_response.text)["refresh_token"]},
        )

    assert response.status_code == 200
    response_json: dict = json.loads(response.text)
    assert "access_token" in response_json.keys()
    assert "refresh_token" in response_json.keys()
    assert "token_type" in response_json.keys()


@pytest.mark.asyncio
async def test_expired_token_refresh():
    await build_db_client()

    # Add any expired token.
    expired_refresh_token = ""

    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/auth/refresh", json={"refresh_token": expired_refresh_token}
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_invalid_token_refresh():
    await build_db_client()

    # Add any invalid token.
    invalid_refresh_token = ""

    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/auth/refresh", json={"refresh_token": invalid_refresh_token}
        )

    assert response.status_code == 403
