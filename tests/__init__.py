from typing import Final
from src.app import fastapi_app
from src.db.connection import build_client as build_db_client
from os import environ

BASE_URL: Final[str] = "http://test"

environ['SECRET_KEY']='test-secret-key'