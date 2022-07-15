from pydantic import BaseModel


class BaseMessage(BaseModel):
    """Base class to define a return messge."""

    message: str
