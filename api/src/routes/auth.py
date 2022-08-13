from datetime import timedelta
from os import environ
from typing import Any, Dict, Final

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose.exceptions import JWTError
from pydantic import BaseModel
from src.core import auth
from src.core.exceptions import DecodeTokenError, ValidateTokenError
from src.db.collections import user as db_user
from src.helpers.container import CONTAINER
from src.models.auth import AuthMessage
from src.models.commons import HttpExceptionMessage
from src.models.user import UserLogin
from src.routes.enums.commons import Endpoint
from src.services.logger.interfaces.i_logger import ILogger

# Router instantiation.
router = APIRouter()

# Constant initialization.
_LOGIN_POST_PARAMS: Final[Dict[Endpoint, Any]] = {
    Endpoint.RESPONSE_MODEL: AuthMessage,
    Endpoint.RESPONSES: {
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            "description": "Unsuccesful login, wrong email or password",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An errorr occured during the token creation",
        },
    },
    Endpoint.DESCRIPTION: "Authenticate an user given username and password to return a set of access and refresh tokens after a succesful validation.",
}


@router.post(
    "/login",
    response_model=_LOGIN_POST_PARAMS[Endpoint.RESPONSE_MODEL],
    responses=_LOGIN_POST_PARAMS[Endpoint.RESPONSES],
    description=_LOGIN_POST_PARAMS[Endpoint.DESCRIPTION],
)
async def login(
    request_form: OAuth2PasswordRequestForm = Depends(),
):
    logger = CONTAINER.get(ILogger)
    response: BaseModel
    status_code: int

    # Query to get the requested user.
    user_res = await db_user.User.find_one(
        db_user.User.username == request_form.username
    )

    msg = "Invalid username or password"
    # Search if user exists in DB.
    # The user does not exists.

    if user_res is None:
        logger.warning("routes", f"{request_form.username} user not found in database.")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=msg)

    # A projecton is not made because the password is required to check if the user has th
    user_projection = UserLogin(
        email=user_res.email, username=user_res.username, roles=user_res.roles
    )

    # Check if the input password match the stored one,
    # but before doing so the password to check must be hashed, and then compared.
    if not auth.verify_password(
        # request_form.password, DB_USERS[request_form.username]["password"]
        request_form.password,
        user_res.password,
    ):
        logger.warning("routes", f"Wrong password for {request_form.username}.")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=msg)

    # The user exists.
    # Converting expriation times to timedelta.
    try:
        access_timedelta = timedelta(minutes=auth.JWT_CONFIG["access_expiration"])
        refresh_timedelta = timedelta(minutes=auth.JWT_CONFIG["refresh_expiration"])
    except KeyError as e:
        msg = f"An error occured while retriving the tokens expiration times"
        logger.error("routes", f"{msg}: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)

    # Generating access and refresh tokens.
    try:
        access_token = auth.create_token(
            user_projection.dict(),
            access_timedelta,
            False,
            environ["SECRET_KEY"],
            auth.JWT_CONFIG["algorithm"],
        )
        refresh_token = auth.create_token(
            user_projection.dict(),
            refresh_timedelta,
            True,
            environ["SECRET_KEY"],
            auth.JWT_CONFIG["algorithm"],
        )
    except KeyError as e:
        msg = f"An error occured while retriving the secret or the algorithm to encode the tokens"
        logger.error("routes", f"{msg}: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    except JWTError as e:
        msg = f"An error occured while encoding the tokens"
        logger.error("routes", f"{msg}: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)

    response = AuthMessage(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
    status_code = status.HTTP_200_OK

    logger.info(
        "routes", f"Successfully generated token for {user_projection.username}"
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


_REFRESH_POST_PARAMS: Final[Dict[Endpoint, Any]] = {
    Endpoint.RESPONSE_MODEL: AuthMessage,
    Endpoint.RESPONSES: {
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            "description": "The token contains informations of unexisting user which is not in the database.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HttpExceptionMessage,
            "description": "Unsuccesfull refresh, the token may be expired, invalid or not a refresh token.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An error occured while refreshing the token",
        },
    },
    Endpoint.DESCRIPTION: "Token refresh route to provide a new set of access and refresh token. The new set will be generated from the refresh token, if this one is expired then login is newly required.",
}


@router.post(
    "/refresh",
    response_model=_REFRESH_POST_PARAMS[Endpoint.RESPONSE_MODEL],
    responses=_REFRESH_POST_PARAMS[Endpoint.RESPONSES],
    description=_REFRESH_POST_PARAMS[Endpoint.DESCRIPTION],
)
async def refresh(
    refresh_token: str | None = Header(default=None),
):
    logger = CONTAINER.get(ILogger)
    response: BaseModel
    status_code: int
    decoded_token: dict
    msg: str

    # Decode token.
    try:
        decoded_token = auth.decode_token(refresh_token)
        logger.debug("routes", f"Decoded token {decoded_token}")
    except DecodeTokenError as e:
        logger.warning("routes", e.loggable)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.msg)

    # Validate the token.
    try:
        _ = auth.valid_refresh_token(decoded_token)
    except ValidateTokenError as e:
        logger.warning("routes", e.loggable)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.msg)

    # If username not in db raise exception.
    user_res = await db_user.User.find_one(
        db_user.User.username == decoded_token["username"]
    )

    if user_res is None:
        logger.warning(
            "routes", f"{decoded_token.get('username')} user not found in database."
        )
        msg = "The token contains informations of an unexisting user."
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=msg)

    # The token is valid and is about an existing user, generate a new token pair.

    # A projecton is not made because the password is required to check if the user has th
    user_projection = UserLogin(
        email=user_res.email, username=user_res.username, roles=user_res.roles
    )

    # Converting expriation times to timedelta.
    try:
        access_timedelta = timedelta(minutes=auth.JWT_CONFIG["access_expiration"])
        refresh_timedelta = timedelta(minutes=auth.JWT_CONFIG["refresh_expiration"])
    except KeyError as e:
        msg = f"An error occured while retriving the tokens expiration times"
        logger.error("routes", f"{msg}: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)

    # Generating access and refresh tokens.
    try:
        new_access_token = auth.create_token(
            user_projection.dict(),
            access_timedelta,
            False,
            environ["SECRET_KEY"],
            auth.JWT_CONFIG["algorithm"],
        )
        new_refresh_token = auth.create_token(
            user_projection.dict(),
            refresh_timedelta,
            True,
            environ["SECRET_KEY"],
            auth.JWT_CONFIG["algorithm"],
        )
    except KeyError as e:
        msg = f"An error occured while retriving the secret or the algorithm to encode the tokens"
        logger.error("routes", f"{msg}: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    except JWTError as e:
        msg = f"An error occured while encoding the tokens"
        logger.error("routes", f"{msg}: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)

    # Generate new token pair.
    response = AuthMessage(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )
    status_code = status.HTTP_200_OK

    logger.info(
        "routes", f"Successfully refreshed token for {user_projection.username}"
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))
