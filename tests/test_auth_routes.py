from fastapi import FastAPI
from tests import fastapi_client


def test_login():
    response = fastapi_client.post("/auth/login", json={"username": "admin", "password": "admin"})
    assert False