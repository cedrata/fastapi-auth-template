from typing import Any, Dict, Final

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# from src.helpers.container import CONTAINER
# from typing import Any
from fastapi.security import OAuth2PasswordRequestForm

# from src.mock.fake_db import DB_USERS
from src.models.commons import BaseMessage
from src.models.auth import AuthMessage
from src.routes.enums.commons import Endpoint

# Constant initialization.
_LOGIN_POST_PARAMS: Final[Dict[Endpoint, Any]] = {
    Endpoint.RESPONSE_MODEL: AuthMessage,
    Endpoint.RESPONSES: {
        status.HTTP_403_FORBIDDEN: {
            "model": BaseMessage,
            "description": "Unsuccesful login, wrong email or password",
        }
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
# @router.post("/login")
async def login(request_form: OAuth2PasswordRequestForm = Depends()):
    # Search if user exists in DB. If not throw error.
    # Search if pwd match. If not return HTTPEception.
    # If user exists and pwd match return:
    #   - Status code.
    #   - AccessToken.
    #   - RefreshToken.
    pippo = True
    response: Any
    status_code: int
    if not pippo:
        response = BaseMessage(message="Authorization failed")
        status_code = status.HTTP_403_FORBIDDEN
    else:
        response = AuthMessage(
            access_token="access token", refresh_token="refresh token"
        )
        status_code = status.HTTP_200_OK

    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))
