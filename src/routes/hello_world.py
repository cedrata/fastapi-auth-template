from fastapi import APIRouter, status
from src.helpers.container import CONTAINER
from src.models.commons import BaseMessage
from src.services.logger.interfaces.i_logger import ILogger

router = APIRouter()


@router.get("/", response_model=BaseMessage, status_code=status.HTTP_200_OK)
async def root():
    log = CONTAINER.get(ILogger)
    log.info("some", "Hello world")
    return BaseMessage(message="Hello, world! (Simple message type)")
