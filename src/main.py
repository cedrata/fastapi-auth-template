from typing import Final

from fastapi import FastAPI

from src.routes.hello_world import router as hello_world_router

# Move to config file.
reoutes_prefix: Final[str] = "/cdrt"

app = FastAPI()

app.include_router(hello_world_router, prefix=reoutes_prefix, tags=["Root"])
