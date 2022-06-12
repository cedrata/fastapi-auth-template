from app.models.core import SimpleMessage
from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_model=SimpleMessage)
async def root():
    return SimpleMessage(message="Hello, world! (Simple message type)")
