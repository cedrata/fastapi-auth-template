from pydantic import BaseModel


class LoggerConfig(BaseModel):
    """
    Python logging configuration model.

    Args:
        BaseModel (pydantic.BaseModel): PydanticBase model.
    """
    ...