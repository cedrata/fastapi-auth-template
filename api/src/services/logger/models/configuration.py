from typing import Optional

from pydantic import BaseModel
from src.services.logger.enums.level import LogLevel


class BaseLogConfig(BaseModel):
    # This format string has the same syntax as the
    # default python logging format string.
    format: str
    level: Optional[LogLevel] = LogLevel.NOTSET


class BaseFileLogConfig(BaseLogConfig):
    # The log file name where the output will be
    # printed for the given configuration.
    filename: str


class TimedRotatingFileConfig(BaseFileLogConfig):
    # Check the python logging.handler.TimedRotatingFileHandler
    # documentation to know about each attribute.
    when: Optional[str] = None
    interval: Optional[int] = 1
    backup_count: Optional[int] = 0
    encoding: Optional[str] = None
    delay: Optional[bool] = False
    utc: Optional[bool] = False
    atTime: Optional[bool] = None
    errors: Optional[bool] = None
