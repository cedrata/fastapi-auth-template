from datetime import timedelta
from typing import Final

from jose import jwt
from src.core.auth import create_token, hash_password, verify_password

PLAIN_PASSWORD: Final[str] = "test-pwd"
USER: Final[dict] = {"username": "mariorossi", "password": "secure-hashed-pwd"}
SECRET_KEY: Final[str] = "secret-key"


def test_hashing():
    assert PLAIN_PASSWORD != hash_password(PLAIN_PASSWORD)


def test_verify_password():
    hashed_password = hash_password(PLAIN_PASSWORD)
    assert verify_password(PLAIN_PASSWORD, hashed_password)


def test_create_token():
    exp_delta = timedelta(minutes=5)

    token = create_token(
        data=USER,
        expires_delta=exp_delta,
        secret_key=SECRET_KEY,
        algorithm="HS256",
    )

    try:
        decoded_token: dict = jwt.decode(
            token=token, key=SECRET_KEY, algorithms="HS256"
        )
        assert decoded_token == {**USER, "exp": decoded_token["exp"]}
    except:
        assert False
