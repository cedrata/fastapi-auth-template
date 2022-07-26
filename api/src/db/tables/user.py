from typing import List

from beanie import Document, Indexed


class User(Document):
    username: Indexed(str)
    password: str
    roles: List[str]

    class Settings:
        name = "users"
