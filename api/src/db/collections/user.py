from datetime import datetime
from typing import List

from beanie import Document, Indexed


class User(Document):
    email: Indexed(str)
    username: Indexed(str)
    password: str
    roles: List[str]
    creation: datetime
    last_update: datetime


    class Settings:
        name = "users"
