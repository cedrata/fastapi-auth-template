from typing import Any, Final

import typesentry
from fastapi import Depends, HTTPException, status
from src.core.auth import OAUTH2_SCHEME, decode_token, has_roles, valid_access_token
from src.core.exceptions import DecodeTokenError
from src.helpers.container import CONTAINER
from src.models.user import Role
from src.services.logger.interfaces.i_logger import ILogger

_TC: Final[typesentry.Config] = typesentry.Config()
IS_TYPED: Final[Any] = _TC.is_type


def is_authorized(token: str = Depends(OAUTH2_SCHEME)) -> bool:
    """This function will check if an user is authorized or not.

    Args:
        token (str, optional): Token read from the header. Defaults to Depends(OAUTH2_SCHEME).

    Raises:
        HTTPException: When the token is invalid an exception is thrown.

    Returns:
        bool: True if the user is authenticated (valid token), False otherwise.
    """
    logger = CONTAINER.get(ILogger)
    decoded_token: dict
    try:
        decoded_token = decode_token(token)
    except DecodeTokenError as e:
        logger.warning("routes", e.loggable)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=e.msg)
    return valid_access_token(decoded_token)


def is_admin(token: str = Depends(OAUTH2_SCHEME)) -> bool:
    """This function will check if an user is authorized and has admin role.

    Args:
        token (str, optional): Token read from the header. Defaults to Depends(OAUTH2_SCHEME).

    Raises:
        HTTPException: When the token is invalid or missing an exception is thrown.

    Returns:
        bool: True when the user is authenticated and is admin, False when is authenticated but not admin.
    """
    logger = CONTAINER.get(ILogger)
    decoded_token: dict
    try:
        decoded_token = decode_token(token)
    except DecodeTokenError as e:
        logger.warning("routes", e.loggable)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=e.msg)

    if not valid_access_token(decoded_token):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if not has_roles(decoded_token["roles"], [Role.ADMIN]):
        return False

    return True


async def require_admin(token: str = Depends(OAUTH2_SCHEME)) -> None:
    """This function aim to check if a user has the admin role. If not an HttpException will be raised.

    Args:
        authorization (str | None, optional): Authorization string. Defaults to Header(default=None).

    Raises:
        HTTPException: Exception to indicate that the autentication did not went as expected.
    """

    logger = CONTAINER.get(ILogger)
    decoded_token: dict
    try:
        decoded_token = decode_token(token)
    except DecodeTokenError as e:
        logger.warning("routes", e.loggable)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=e.msg)

    if not valid_access_token(decoded_token):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if not has_roles(decoded_token["roles"], [Role.ADMIN]):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Forbiddent access, required role: ADMIN"
        )
