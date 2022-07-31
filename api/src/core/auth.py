import sys
from datetime import datetime, timedelta
from os import environ
from os.path import join
from typing import Any, Dict, Final

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from src.helpers.container import CONTAINER
from src.services.logger.interfaces.i_logger import ILogger
from yaml import safe_load

# This is instance will be injected in routes when those have to be secured.
# This is just checcking the user exists and the inserted credentials are corect, role is not
# responsability of OAUTH2_SCHEME, at least for the implementation w/out full oauth flow.
#
# The tokenUrl is not inserted in any configuration file because it should not change in time,
# by doing so it encourages keep the same endpoint as the login one.
OAUTH2_SCHEME: Final = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)

_PWD_CONTEX: Final = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Read configuration file for jwt configuration.
JWT_CONFIG: Final[Dict[str, Any]]
try:
    config_file_path = join(environ["CONFIGS_DIR"], "auth", "jwt_details.yaml")
    with open(config_file_path) as config_file_stream:
        JWT_CONFIG = safe_load(config_file_stream)
except Exception as e:
    logger = CONTAINER.get(ILogger)
    logger.critical(
        "errors", f"An error occured while reading the configuration file in {__file__}"
    )
    sys.exit()

TOKEN_FIELDS: Final[set] = {"username", "roles", "exp", "is_refresh"}


def hash_password(password: str) -> str:
    """Returning the given password with hash."""
    return _PWD_CONTEX.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _PWD_CONTEX.verify(plain_password, hashed_password)


def create_token(
    data: dict,
    expires_delta: timedelta,
    is_refresh: bool,
    secret_key: str,
    algorithm: str,
) -> str:
    """Return a token for the given data, this function can be used to return both access and refresh tokens.
    !!!IMPORTANT!!!
    If "data" argument contains a password make sure it is hashed and not plain!!!

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
    to_encode.update({"is_refresh": is_refresh})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt