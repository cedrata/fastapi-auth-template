from datetime import datetime, timedelta
from typing import Final

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

# This is instance will be injected in routes when those have to be secured.
# This is just checcking the user exists and the inserted credentials are corect, role is not
# responsability of OAUTH2_SCHEME, at least for the implementation w/out full oauth flow.
#
# The tokenUrl is not inserted in any configuration file because it should not change in time,
# by doing so it encourages keep the same endpoint as the login one.
OAUTH2_SCHEME: Final[OAuth2PasswordBearer] = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def hash_password(password: str) -> str:
    """Returning the given password with hash."""
    # TODO: Implement password hashing.
    return password


def create_token(
    data: dict, expires_delta: timedelta, secret_key: str, algorithm: str
) -> str:
    """Return a token for the given data, this function can be used to return both access and refresh tokens.

    Args:
        data (dict): data to encode in jwt.
        expires_delta (timedelta): expiration time expressed in timedelta.
        secret_key (str): secret key to apply signature to jwt.
        algorithm (str): desired encription algoritm.

    Returns:
        str: _description_
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt
