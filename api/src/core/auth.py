import sys
from datetime import datetime, timedelta
from os import environ
from os.path import join
from typing import Any, Dict, Final

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from passlib.context import CryptContext
from src.core.exceptions import DecodeTokenError, ValidateTokenError
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

TOKEN_FIELDS: Final[set] = {"email", "username", "roles", "exp", "is_refresh"}


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


def decode_token(encoded_token: str) -> dict:
    """This function will decode a given token and say wether is valid or not.

    Args:
        encoded_token (str): token to decode.

    Raises:
        DecodeTokenError: if anything goes an HTTPException is returned.

    Returns:
        dict: a dictionary containing the decoded_token.
    """

    # This function is tested when testing the /auth/refresh route.
    decoded_token: dict
    try:
        decoded_token = jwt.decode(
            token=encoded_token,
            key=environ["SECRET_KEY"],
            algorithms=JWT_CONFIG["algorithm"],
        )
    except ExpiredSignatureError as e:
        msg = "The provided token is expired"
        raise DecodeTokenError(loggable=str(e), msg=msg)
    except JWTError as e:
        msg = "The provided token is invalid, or cyphered with a different key."
        raise DecodeTokenError(loggable=str(e), msg=msg)
    except Exception as e:
        msg = "An unknown error occured while decoding the token, make sure you are passing a valid and not expired token."
        raise DecodeTokenError(loggable=str(e), msg=msg)

    return decoded_token


def validate_token_base(decoded_token: dict) -> bool:
    """This function will say if the keys present inside the decoded_token are the same that is expected to have a valid token.

    Args:
        decoded_token (dict): decoded token in form of dictionary.

    Raises:
        ValidateTokenError: if the token does not respect the current token structure.

    Returns:
        bool: True if the decoded token structure is valid.
    """
    if TOKEN_FIELDS != set(decoded_token):
        raise ValidateTokenError(
            loggable="The given token keys does not match the keys in src.core.auth.TOKEN_FIELDS.",
            msg="The given token has an invalid structure.",
        )
    return True


def validate_refresh_token(decoded_token: dict) -> bool:
    """This function will see if the token structure (present keys) are valid to then check if the "is_refresh" key is set to false.

    Args:
        decoded_token (dict): decoded token in form of dictionary.

    Raises:
        ValidateTokenError: if the provided token is not a refresh token.

    Returns:
        bool: True if "is_refresh" is True, False otherwise.
    """
    _ = validate_token_base(decoded_token)

    if decoded_token["is_refresh"] is False:
        raise ValidateTokenError(
            loggable="The current token has the 'is_refresh' field set to false.",
            msg="The given token is not a refresh token.",
        )
    return True
