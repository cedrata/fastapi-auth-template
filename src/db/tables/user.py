from typing import List

from beanie import Document

class User(Document):
    username: str
    password: str
    roles: List[str]

    class Settings:
        name = "users"