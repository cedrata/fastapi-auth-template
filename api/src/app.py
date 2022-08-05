from fastapi import FastAPI

from src.db.connection import build_client
from src.routes.auth import router as auth_router
from src.routes.hello_world import router as hello_world_router
from src.routes.user import router as user_router

fastapi_app = FastAPI()

# Injecting routers into app.
fastapi_app.include_router(hello_world_router, prefix="/cdrt", tags=["Hello, world!"])
fastapi_app.include_router(auth_router, prefix="/auth", tags=["Auth"])
fastapi_app.include_router(user_router, prefix="/user", tags=["User"])


@fastapi_app.on_event("startup")
async def app_init():
    # Execute db connection.
    await build_client()
