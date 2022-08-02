import logging
import sys
from logging import Logger, getLogger
from logging.handlers import TimedRotatingFileHandler
from os import environ
from os import mkdir as os_mkdir
from os.path import exists as os_path_exists
from os.path import isfile as os_path_isfile
from os.path import join as os_path_join
from typing import Dict, Final, Optional

from src.services.logger.enums.level import LogLevel
from src.services.logger.models.configuration import TimedRotatingFileConfig
from yaml import safe_load

DEFAULT_LOG_FILE: Final[str] = os_path_join(environ["LOGGING_DIR"], "default.log")
DEFAULT_LOG_LEVEL: Final[str] = LogLevel.DEBUG
DEFAULT_LOG_FORMAT: Final[str] = logging.Formatter("%(levelname)s-%(message)s")
DEFAULT_CONFIG_KEY: Final[str] = "default"
DEFAULT_CONFIG_VALUE: Final[str] = None
DEFAULT_CONFIG_VALUE_TYPE: Final[str] = type(DEFAULT_CONFIG_VALUE)

if not os_path_exists(environ["LOGGING_DIR"]):
    os_mkdir(environ["LOGGING_DIR"])


class TimedLogger:
    """
    Implementation of the ILogger interface using
    the already existing logging facility.
    """

    # Private attributes.
    # _avaiable_loggers: List[str]
    _avaiable_configs: Optional[
        Dict[str, TimedRotatingFileConfig | DEFAULT_CONFIG_VALUE_TYPE]
    ] = None

    def __init__(self, config_file_path: Optional[str] = None) -> None:
        """
        Create a new CdrtLogger with an empty list of avaiable loggers.
        If no configurations is passed, the default configuration is applied.

        Args:
            config_file_path (Optional[str], optional): _description_. Defaults to None.
        """

        # self._avaiable_loggers = []
        self._avaiable_configs = {}
        self._avaiable_configs.setdefault(DEFAULT_CONFIG_KEY, DEFAULT_CONFIG_VALUE)
        if config_file_path is not None:
            self.file_config(config_file_path)
        # Fallback, if configuration file is none.
        else:
            new_logger = getLogger(DEFAULT_CONFIG_KEY)
            self._apply_default_config(new_logger)

    @staticmethod
    def _log_level_mapper(log_level: LogLevel) -> int:
        """
        Parse the LogLevel enum to the logging default enum.

        Args:
            log_level (LogLevel): log level to parse.
        """
        match log_level:
            case LogLevel.NOTSET:
                return logging.NOTSET
            case LogLevel.DEBUG:
                return logging.DEBUG
            case LogLevel.INFO:
                return logging.INFO
            case LogLevel.WARNING:
                return logging.WARNING
            case LogLevel.ERROR:
                return logging.ERROR
            case LogLevel.CRITICAL:
                return logging.CRITICAL

    def file_config(self, config_file_path: str) -> None:
        """
        Configure the given logger with a valid configuration file.

        Args:
            config_file_path (str): absolute path of the configuration file.
        """

        if not os_path_exists(config_file_path) or not os_path_isfile(config_file_path):
            raise FileNotFoundError

        # Reading all the configurations.
        configurations: dict = {}
        try:
            with open(config_file_path, "r") as config_file_sream:
                configurations = safe_load(config_file_sream)
        except Exception as e:
            print(e)
            sys.exit()

        # Adding the configurations to the avaiable configurations.
        for k, v in configurations.items():
            self._avaiable_configs[k] = TimedRotatingFileConfig.parse_obj(v)
            new_logger = getLogger(k)
            self._apply_custom_timed_config(new_logger, self._avaiable_configs[k])

        # Fallback, if the configuration file was empty then apply a default configuration.
        if len(configurations.keys()) == 0:
            new_logger = getLogger(DEFAULT_CONFIG_KEY)
            self._apply_default_config(new_logger)

    def debug(self, logger_name: str, message: str) -> None:
        """
        Print a debug level log statement with the specified logger.

        Args:
            logger_name (str): the logger name to use.
            message (str): the message to log.
        """
        if logger_name in self._avaiable_configs.keys():
            logger = logging.getLogger(logger_name)
            logger.debug(message)
        else:
            logging.debug(message)

    def info(self, logger_name: str, message: str) -> None:
        """
        Print an info level log statement with the specified logger.

        Args:
            logger_name (str): the logger name to use.
            message (str): the message to log.
        """
        if logger_name in self._avaiable_configs.keys():
            logger = logging.getLogger(logger_name)
            logger.info(message)
        else:
            logging.info(message)

    def warning(self, logger_name: str, message: str) -> None:
        """
        Print a warning level log statement with the specified logger.

        Args:
            logger_name (str): the logger name to use.
            message (str): the message to log.
        """
        if logger_name in self._avaiable_configs.keys():
            logger = logging.getLogger(logger_name)
            logger.warning(message)
        else:
            logging.warning(message)

    def error(self, logger_name: str, message: str) -> None:
        """
        Print an error level log statement with the specified logger.

        Args:
            logger_name (str): the logger name to use.
            message (str): the message to log.
        """
        if logger_name in self._avaiable_configs.keys():
            logger = logging.getLogger(logger_name)
            logger.error(message)
        else:
            logging.error(message)

    def critical(self, logger_name: str, message: str) -> None:
        """
        Print critical level log statement with the specified logger.

        Args:
            logger_name (str): the logger name to use.
            message (str): the message to log.
        """
        if logger_name in self._avaiable_configs.keys():
            logger = logging.getLogger(logger_name)
            logger.critical(message)
        else:
            logging.critical(message)

    # Private methods.
    def _apply_default_config(self, new_logger: Logger) -> None:
        """
        Apply a default configuration to the given logger.

        Args:
            new_logger (Logger): to handle logger.
        """
        new_logger.setLevel(self._log_level_mapper(DEFAULT_LOG_LEVEL))
        handler = TimedRotatingFileHandler(DEFAULT_LOG_FILE)
        fmt = DEFAULT_LOG_FORMAT
        handler.setFormatter(fmt)

        new_logger.addHandler(handler)

    def _apply_custom_timed_config(
        self, new_logger: Logger, config: TimedRotatingFileConfig
    ) -> None:
        """
        Apply a custom configuration to the given logger.

        Args:
            new_logger (Logger): logger to configure.
            config (TimedRotatingFileConfig): logger configurations.
        """
        new_logger.setLevel(self._log_level_mapper(config.level))
        handler = TimedRotatingFileHandler(
            os_path_join(environ["LOGGING_DIR"], config.filename),
            config.when,
            config.interval,
            config.backup_count,
            config.encoding,
            config.delay,
            config.utc,
            config.atTime,
            config.errors,
        )
        fmt = logging.Formatter(config.format)
        handler.setFormatter(fmt)

        new_logger.addHandler(handler)
