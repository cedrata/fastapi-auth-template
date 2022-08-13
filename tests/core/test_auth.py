from datetime import timedelta
from typing import Final

from jose import jwt
from src.core.auth import (
    create_token,
    has_roles,
    hash_password,
    valid_access_token,
    valid_refresh_token,
    valid_token,
    verify_password,
)
from src.models.user import Role

PLAIN_PASSWORD: Final[str] = "test-pwd"
USER: Final[dict] = {"username": "mariorossi", "password": "secure-hashed-pwd"}
SECRET_KEY: Final[str] = "secret-key"


def test_hashing():
    assert PLAIN_PASSWORD != hash_password(PLAIN_PASSWORD)


def test_verify_password():
    hashed_password = hash_password(PLAIN_PASSWORD)
    assert verify_password(PLAIN_PASSWORD, hashed_password)


def test_verify_bad_password():
    hashed_password = hash_password(PLAIN_PASSWORD)
    assert not verify_password("bad-pwd", hashed_password)


def test_create_token():
    exp_delta = timedelta(minutes=5)

    token = create_token(
        data=USER,
        expires_delta=exp_delta,
        secret_key=SECRET_KEY,
        is_refresh=True,
        algorithm="HS256",
    )

    try:
        decoded_token: dict = jwt.decode(
            token=token, key=SECRET_KEY, algorithms="HS256"
        )
        assert decoded_token == {
            **USER,
            "exp": decoded_token["exp"],
            "is_refresh": True,
        }
    except:
        assert False


def test_valid_token():
    test_decoded_token = {
        "email": "",
        "username": "",
        "roles": "",
        "exp": "",
        "is_refresh": "True",
        "is_refresh": "",
    }
    assert valid_token(test_decoded_token)


def test_valid_refresh_token():
    test_decoded_token = {
        "email": "",
        "username": "",
        "roles": "",
        "exp": "",
        "is_refresh": "True",
        "is_refresh": True,
    }
    assert valid_refresh_token(test_decoded_token)


def test_valid_access_token():
    test_decoded_token = {
        "email": "",
        "username": "",
        "roles": "",
        "exp": "",
        "is_refresh": "True",
        "is_refresh": False,
    }
    assert valid_access_token(test_decoded_token)


def test_has_roles():
    assert has_roles(user_roles=[Role.ADMIN], required_roles=[Role.ADMIN])


def test_has_bad_roles():
    assert not has_roles(user_roles=[Role.USER], required_roles=[Role.ADMIN])
