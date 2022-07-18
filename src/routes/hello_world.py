from os import environ
from fastapi import APIRouter, status, Depends
from jose import JWTError
from src.helpers.container import CONTAINER
from src.models.commons import BaseMessage
from src.core.auth import OAUTH2_SCHEME
from src.services.logger.interfaces.i_logger import ILogger
from jose import jwt

router = APIRouter()


@router.get("/", response_model=BaseMessage, status_code=status.HTTP_200_OK)
async def root():
    log = CONTAINER.get(ILogger)
    log.info("some", "Hello world")
    return BaseMessage(message="Hello, world! (Simple message type)")

@router.get("/test-auth")
async def test_auth(token: str = Depends(OAUTH2_SCHEME)):
    return jwt.decode(token, environ['SECRET_KEY'], algorithms='HS256')