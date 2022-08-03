from fastapi import APIRouter
from src.models.user import UserRegistration

router = APIRouter()


@router.post("/register")
async def register(user: UserRegistration):
    ...
