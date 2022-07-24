from typing import List

from pydantic import BaseModel


class UserLogin(BaseModel):
    """Class for projection with only username and roles (other attributes if required, no password), from the db users collection."""

    username: str
    roles: List[str]
