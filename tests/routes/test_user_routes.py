from datetime import datetime
from json import JSONDecodeError
from typing import List

import pytest
from httpx import AsyncClient
from pydantic import parse_raw_as
from src.db.collections.user import User
from src.models.user import (
    CurrentUserDetails,
    UserPartialDetails,
    UserPartialDetailsAdmin,
)
from tests import (
    BASE_URL,
    admin_login,
    build_db_client,
    fastapi_app,
    user_login,
    IS_TYPED,
)


@pytest.mark.asyncio
async def test_register():

    # DB connection.
    await build_db_client()

    # Endpoint test
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register",
            json={
                "username": "new_test_user",
                "email": "new_test_user@email.com",
                "password": "new_test_user",
            },
        )
    assert response.status_code == 201

    # Clearing environement.
    await User.find_one(User.username == "new_test_user").delete()


@pytest.mark.asyncio
async def test_register_duplicate_email():

    # DB connection.
    await build_db_client()

    # Add values to test the db.
    now_date = datetime.utcnow()
    await User(
        email="new_test_user@email.com",
        username="new_test_user",
        password="new_test_user",
        roles=["user"],
        creation=now_date,
        last_update=now_date,
    ).save()

    # Endpoint test
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register",
            json={
                "username": "different_username",
                "email": "new_test_user@email.com",
                "password": "new_test_user",
            },
        )
    assert response.status_code == 409

    # Clearing environement.
    await User.find_one(User.username == "new_test_user").delete()


@pytest.mark.asyncio
async def test_register_duplicate_username():

    # DB connection.
    await build_db_client()

    # Add values to test the db.
    now_date = datetime.utcnow()
    await User(
        email="new_test_user@email.com",
        username="new_test_user",
        password="new_test_user",
        roles=["user"],
        creation=now_date,
        last_update=now_date,
    ).save()

    # Endpoint test
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register",
            json={
                "username": "new_test_user",
                "email": "different@email.com",
                "password": "new_test_user",
            },
        )
    assert response.status_code == 409

    # Clearing environement.
    await User.find_one(User.username == "new_test_user").delete()


@pytest.mark.asyncio
async def test_register_admin():

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register-roles",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "new_test_user_admin",
                "email": "new_test_user_admin@email.com",
                "password": "new_test_user_admin",
                "roles": ["admin", "user"],
            },
        )
    assert response.status_code == 201

    # Clearing environement.
    await User.find_one(User.username == "new_test_user_admin").delete()


@pytest.mark.asyncio
async def test_register_admin_wrong_roles():

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register-roles",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "missing_role_user",
                "email": "missing_role_user@email.com",
                "password": "missing_role_user",
                "roles": ["admina"],
            },
        )
    assert response.status_code == 422

    # Clearing environement.
    # Not needed because no elements have been added to DB.


@pytest.mark.asyncio
async def test_register_admin_missing_roles():

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register-roles",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "missing_role_user",
                "email": "missing_role_user@email.com",
                "password": "missing_role_user",
            },
        )
    assert response.status_code == 422

    # Clearing environement.
    # Not needed because no elements have been added to DB.


@pytest.mark.asyncio
async def test_register_admin_duplicate_email():

    # DB connection.
    await build_db_client()

    # Add values to test the db.
    now_date = datetime.utcnow()
    await User(
        email="new_test_user_admin@email.com",
        username="new_test_user_admin",
        password="new_test_user",
        roles=["user"],
        creation=now_date,
        last_update=now_date,
    ).save()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register-roles",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "duplicate_test_user_admin",
                "email": "new_test_user_admin@email.com",
                "password": "new_test_user_admin",
                "roles": ["admin", "user"],
            },
        )
    assert response.status_code == 409

    # Clearing environement.
    await User.find_one(User.username == "new_test_user_admin").delete()


@pytest.mark.asyncio
async def test_register_admin_duplicate_username():

    # DB connection.
    await build_db_client()

    # Add values to test the db.
    now_date = datetime.utcnow()
    await User(
        email="new_test_user_admin@email.com",
        username="new_test_user_admin",
        password="new_test_user",
        roles=["user"],
        creation=now_date,
        last_update=now_date,
    ).save()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/user/register-roles",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
            json={
                "username": "new_test_user_admin",
                "email": "duplicate_test_user_admin@email.com",
                "password": "new_test_user_admin",
                "roles": ["admin", "user"],
            },
        )
    assert response.status_code == 409

    # Clearing environement.
    await User.find_one(User.username == "new_test_user_admin").delete()


@pytest.mark.asyncio
async def test_get_all_users():

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.get(
            "/user/all",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200
    assert IS_TYPED(
        parse_raw_as(List[UserPartialDetails], response.text), List[UserPartialDetails]
    )


@pytest.mark.asyncio
async def test_get_all_user_as_admin():

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.get(
            "/user/all",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200
    assert IS_TYPED(
        parse_raw_as(List[UserPartialDetailsAdmin], response.text),
        List[UserPartialDetailsAdmin],
    )


@pytest.mark.asyncio
async def test_get_users_count():

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.get(
            "/user/count",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_by_id_username():

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    # Username
    username = "admin"

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.get(
            f"/user/username/{username}",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200

    found = parse_raw_as(UserPartialDetails, response.text)
    assert found.username == username


@pytest.mark.asyncio
async def test_get_user_by_id_username_as_admin():

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Username
    username = "admin"

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.get(
            f"/user/username/{username}",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200

    found = parse_raw_as(UserPartialDetailsAdmin, response.text)
    assert found.username == username


@pytest.mark.asyncio
async def test_get_current_user():

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.get(
            f"/user/me",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200

    try:
        found = parse_raw_as(CurrentUserDetails, response.text)
        assert found.username == "user"  # The login has made with admin user.
    except JSONDecodeError:
        raise AssertionError(
            f"Impossible to parse to {CurrentUserDetails.__name__} json: {response.text}."
        )

@pytest.mark.asyncio
async def update_user():

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = ac.put(
            f"/user/username/user",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200

@pytest.mark.asyncio
async def update_user_bad():

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await user_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = ac.put(
            f"/user/username/admin",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def update_user_admin():

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = ac.put(
            f"/user/username/user",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 200

@pytest.mark.asyncio
async def update_user_admin_missing():
    # Try to update an user that does not exists.

    # DB connection.
    await build_db_client()

    # Execute login.
    login_response = await admin_login()

    # Endpoint test.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = ac.put(
            f"/user/username/missing",
            headers={
                "Authorization": f"{login_response.token_type} {login_response.access_token}"
            },
        )

    assert response.status_code == 404