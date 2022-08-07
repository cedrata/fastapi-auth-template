from pydantic import BaseModel


class AuthMessage(BaseModel):
    """Class that represent the answer after a succesful authentication."""

    access_token: str
    refresh_token: str
    token_type: str
