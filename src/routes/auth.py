from typing import Any, Dict, Final

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# from src.helpers.container import CONTAINER
# from typing import Any
from fastapi.security import OAuth2PasswordRequestForm
from src.mock.fake_db import DB_USERS
from src.models.auth import AuthMessage

# from src.mock.fake_db import DB_USERS
from src.routes.enums.commons import Endpoint
from src.services.auth import OAUTH2_SCHEME

# Constant initialization.
_LOGIN_POST_PARAMS: Final[Dict[Endpoint, Any]] = {
    Endpoint.RESPONSE_MODEL: AuthMessage,
    Endpoint.RESPONSES: {
        status.HTTP_401_UNAUTHORIZED: {
            # "model": Any if required (not valid to isert http exception here)
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
async def login(request_form: OAuth2PasswordRequestForm = Depends()):
    response: Any
    status_code: int

    error_message = "Invalid username or password"
    # Search if user exists in DB.
    # The user does not exists.
    if not request_form.username in DB_USERS.keys():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=error_message)

    # Check if the input password match the stored one.
    if DB_USERS[request_form.username]["password"] != request_form.password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=error_message)

    # The user exists.
    response = AuthMessage(access_token="success", refresh_token="success", token_type="bearer")
    status_code = status.HTTP_200_OK

    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))