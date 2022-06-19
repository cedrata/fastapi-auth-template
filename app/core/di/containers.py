from sqlite3 import Time
from app.services.logger.interfaces.i_logger import ILogger
from app.services.logger.implementations.logger import TimedLogger
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from sys import modules
from typing import Final
from os.path import join, abspath

ROOT_DIR: Final[str] = abspath('/Users/lucagreggio/Dev/python/fastapi-auth-template/app/core/di/containers.py/../../..')
TIMED_LOGGER_CONFIG_FILENAME: Final[str] = 'custom_log.yaml'
TIMED_LOGGER_CONFIGS_PATH: Final[str] = join(ROOT_DIR, 'services', 'logger', 'configs', TIMED_LOGGER_CONFIG_FILENAME)

class Container(DeclarativeContainer):
    
    log_service: ILogger = Singleton(TimedLogger, TIMED_LOGGER_CONFIGS_PATH)