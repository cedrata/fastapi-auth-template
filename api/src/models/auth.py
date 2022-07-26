from pydantic import BaseModel


class AuthMessage(BaseModel):
    """Class that extend the StatusMessage to access and refresh token."""

    access_token: str
    refresh_token: str
    token_type: str