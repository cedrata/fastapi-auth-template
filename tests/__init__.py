from typing import Final
from src.app import fastapi_app
from src.db.connection import build_client as build_db_client

BASE_URL: Final[str] = "http://test"