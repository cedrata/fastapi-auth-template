from fastapi import APIRouter
from src.helpers.container import CONTAINER
from src.models.core import SimpleMessage
from src.services.logger.interfaces.i_logger import ILogger

router = APIRouter()


@router.get("/", response_model=SimpleMessage)
async def root():
    log = CONTAINER.get(ILogger)
    log.info('some', "Hello world")
    return SimpleMessage(message="Hello, world! (Simple message type)")
