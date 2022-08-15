import sys
from datetime import datetime, timedelta
from os import environ
from os.path import join
from typing import Any, Dict, Final, List, Tuple

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from passlib.context import CryptContext
from src.core.exceptions import DecodeTokenError
from src.helpers.container import CONTAINER
from src.models.user import Role
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
    The password should not be contained in the token anyway.

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


def valid_token(decoded_token: dict) -> bool:
    """This function will say if the keys present inside the decoded_token are the same that is expected to have a valid token.

    Args:
        decoded_token (dict): decoded token in form of dictionary.

    Returns:
        bool: True if the decoded token structure is valid.
    """
    if TOKEN_FIELDS != set(decoded_token):
        return False
    return True


def valid_refresh_token(decoded_token: dict) -> bool:
    """This function will see if the token structure (present keys) are valid to then check if the "is_refresh" key is set to true.

    Args:
        decoded_token (dict): decoded token in form of dictionary.

    Returns:
        bool: True if "is_refresh" is True, False otherwise.
    """
    if not valid_token(decoded_token):
        return False
    if decoded_token["is_refresh"] is False:
        return False
    return True


def valid_access_token(decoded_token: dict) -> bool:
    """This function will see if the token structure (present keys) are valid to then check if the "is_refresh" key is set to false.

    Args:
        decoded_token (dict): decoded token in form of dictionary.

    Returns:
        bool: True if "is_refresh" is False, False otherwise.
    """
    if not valid_token(decoded_token):
        return False
    if decoded_token["is_refresh"] is True:
        return False
    return True


def has_roles(user_roles: List[Role], required_roles: List[Role]) -> bool:
    """This function will check efficiently if the user roles have at least one of the required roles.

    Args:
        user_roles (List[Role]): user roles.
        required_roles (List[Role]): required roles.

    Returns:
        bool: True if at least one of the user roles is contained in the required roles.
    """
    return bool(set(user_roles) & set(required_roles))


def is_authorized(token: str = Depends(OAUTH2_SCHEME)) -> Tuple[bool, dict]:
    """This function will check if an user is authorized or not.

    Args:
        token (str, optional): Token read from the header. Defaults to Depends(OAUTH2_SCHEME).

    Raises:
        HTTPException: When the token is invalid an exception is thrown.

    Returns:
        bool: True if the user is authenticated (has a valid accesss token), False otherwise.
        dict: Dictionary contining the decoded token if is authorized, otherwise empty dictionary.
    """
    # logger = CONTAINER.get(ILogger)
    decoded_token: dict = {}
    try:
        decoded_token = decode_token(token)
    except DecodeTokenError as e:
        # logger.warning("routes", e.loggable)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=e.msg)
    return (valid_access_token(decoded_token), decoded_token)


def is_admin(token: str = Depends(OAUTH2_SCHEME)) -> Tuple[bool, bool, dict]:
    """This function will check if an user is authorized and has admin role.

    Args:
        token (str, optional): Token read from the header. Defaults to Depends(OAUTH2_SCHEME).

    Raises:
        HTTPException: When the token is invalid or missing an exception is thrown.

    Returns:
        bool: True if the user is authenticated (has a valid accesss token), False otherwise.
        bool: True if the user is admin (valid token), False otherwise.
        dict: Dictionary contining the decoded token if is authorized, otherwise empty dictionary.
    """
    authorized, decoded_token = is_authorized(token)

    if not authorized:
        return authorized, False, {}

    if not has_roles(decoded_token["roles"], [Role.ADMIN]):
        return authorized, False, decoded_token

    return authorized, True, decoded_token


def require_admin(token: str = Depends(OAUTH2_SCHEME)) -> None:
    """This function will chck if an user is admin or not, if not raise an HTTPException.

    Args:
        token (str, optional): Token read from the header. Defaults to Depends(OAUTH2_SCHEME).

    Raises:
        HTTPException: Missing authorization or forbidden acces (not admin).
    """
    authorized, admin, _ = is_admin(token)

    if not authorized:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if not admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
