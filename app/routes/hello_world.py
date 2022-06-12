from fastapi import APIRouter

from app.models.core import SimpleMessage

router = APIRouter()

@router.get("/", response_model=SimpleMessage)
async def root():
    return SimpleMessage(message="Hello, world! (Simple message type)")
