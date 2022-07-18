from datetime import timedelta
from os import environ
from typing import Any, Dict, Final

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from src.core import auth
from src.helpers.container import CONTAINER
from src.mock.fake_db import DB_USERS
from src.models.auth import AuthMessage
from src.models.commons import HttpExceptionMessage
from src.routes.enums.commons import Endpoint
from src.services.logger.interfaces.i_logger import ILogger

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
            "description": "Probably an errorr occured during the token creation",
        },
    },
    Endpoint.DESCRIPTION: "Authenticate an user given username and password to return a set of access and refresh tokens after a succesful validation.",
}

# Router instantiation.
router = APIRouter()


@router.post(
    "/login",
    response_model=_LOGIN_POST_PARAMS[Endpoint.RESPONSE_MODEL],
    responses=_LOGIN_POST_PARAMS[Endpoint.RESPONSES],
    description=_LOGIN_POST_PARAMS[Endpoint.DESCRIPTION],
)
async def login(request_form: OAuth2PasswordRequestForm = Depends()):
    logger = CONTAINER.get(ILogger)
    response: Any
    status_code: int

    error_message = "Invalid username or password"
    # Search if user exists in DB.
    # The user does not exists.
    if not request_form.username in DB_USERS.keys():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=error_message)

    # Check if the input password match the stored one,
    # but before doing so the password to check must be hashed, and then compared.
    if DB_USERS[request_form.username]["password"] != auth.hash_password(
        request_form.password
    ):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=error_message)

    # The user exists.
    # Converting expriation times to timedelta.
    try:
        access_timedelta = timedelta(minutes=auth.JWT_CONFIG["access_expiration"])
        refresh_timedelta = timedelta(minutes=auth.JWT_CONFIG["refresh_expiration"])
    except KeyError as e:
        msg = f"An error occured while retriving the tokens expiration times"
        logger.error("auth", f"{msg}: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)

    # Generating access and refresh tokens.
    try:
        access_token = auth.create_token(
            DB_USERS[request_form.username],
            access_timedelta,
            environ["SECRET_KEY"],
            auth.JWT_CONFIG["algorithm"],
        )
        refresh_token = auth.create_token(
            DB_USERS[request_form.username],
            refresh_timedelta,
            environ["SECRET_KEY"],
            auth.JWT_CONFIG["algorithm"],
        )
    except KeyError as e:
        msg = f"An error occured while retriving the secret or the algorithm to encode the tokens"
        logger.error("auth", f"{msg}: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    except JWTError as e:
        msg = f"An error occured while encoding the tokens"
        logger.error("auth", f"{msg}: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)

    response = AuthMessage(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
    status_code = status.HTTP_200_OK

    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))
