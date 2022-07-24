from typing import Final

from fastapi import FastAPI

from src.db.connection import build_client
from src.routes.auth import router as auth_router
from src.routes.hello_world import router as hello_world_router

reoutes_prefix: Final[str] = "/cdrt"

app = FastAPI()


@app.on_event("startup")
async def app_init():
    # Execute db connection.
    await build_client()

    # Injecting routers into app.
    app.include_router(
        hello_world_router, prefix=reoutes_prefix, tags=["Hello, world!"]
    )
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
