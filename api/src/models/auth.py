from pydantic import BaseModel


class AuthMessage(BaseModel):
    """Class that represent the answer after a succesful authentication."""

    access_token: str
    refresh_token: str
    token_type: str


class RefreshMessage(BaseModel):
    """Class that represent the input to generate a new access and refresh token."""

    refresh_token: str
