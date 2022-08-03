from pydantic import BaseModel


class BaseMessage(BaseModel):
    """Base class to define a return messge."""

    message: str


class HttpExceptionMessage(BaseModel):
    """Message model to specify structure in endpoint response when exception is raised."""

    detail: str
