from dataclasses import dataclass
from enum import Enum
from logging import CRITICAL

class LogLevel(Enum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
