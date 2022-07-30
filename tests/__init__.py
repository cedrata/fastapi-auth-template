import asyncio

from fastapi.testclient import TestClient
from src.app import fastapi_app
from src.db.connection import build_client as build_db_client

# Executing async initialization procedures.
_loop = asyncio.new_event_loop()
_loop.run_until_complete(build_db_client())
_loop.close()

# Executing sync initialization procedures.
# Building FastAPI client.
fastapi_client = TestClient(fastapi_app)
