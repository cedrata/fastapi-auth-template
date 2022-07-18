from typing import Final

from fastapi import FastAPI

from src.routes.hello_world import router as hello_world_router
from src.routes.auth import router as auth_router

# Move to config file.
reoutes_prefix: Final[str] = "/cdrt"

app = FastAPI()

app.include_router(hello_world_router, prefix=reoutes_prefix, tags=["Hello, world!"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
