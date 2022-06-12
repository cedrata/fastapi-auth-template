import logging
import sys
from dataclasses import dataclass
from logging import Logger, getLogger
from logging.handlers import TimedRotatingFileHandler
from os.path import dirname as os_path_dirname
from os.path import exists as os_path_exists
from os.path import isfile as os_path_isfile
from os.path import join as os_path_join
from re import I
from typing import Any, Dict, List, Optional

from app.services.logger.enums.level import LogLevel
from app.services.logger.interfaces.i_logger import ILogger
from app.services.logger.models.configuration import TimedRotatingFileConfig
from yaml import safe_load


@dataclass(slots=False)
class TimedLoggerDefaults():
    @staticmethod
    def DEFAULT_LOG_FILE() -> str:
        return os_path_join(os_path_dirname(str(sys.modules['__main__'].__file__)), "default.log")

    @staticmethod
    def DEFAULT_LOG_LEVEL() -> str:
        return LogLevel.DEBUG

    @staticmethod
    def DEFAULT_LOG_FORMAT() -> str:
        return logging.Formatter('%(levelname)s-%(message)s')

    @staticmethod
    def DEFAULT_CONFIG_KEY() -> str:
        return 'default'

    @staticmethod
    def DEFAULT_CONFIG_VALUE() -> Any:
        return None

    @staticmethod
    def DEFAULT_CONFIG_VALUE_TYPE() -> Any:
        return type(TimedLoggerDefaults.DEFAULT_CONFIG_VALUE())


class TimedLogger():
    """
    Implementation of the ILogger interface using
    the already existing logging facility.
    """

    # Private attributes.
    _avaiable_loggers: List[str] 
    _avaiable_configs: Optional[Dict[str, TimedRotatingFileConfig | TimedLoggerDefaults.DEFAULT_CONFIG_VALUE_TYPE()]] = None

    def __init__(self, config_file_path: Optional[str] = None) -> None:
        """
        Create a new CdrtLogger with an empty list of avaiable loggers.
        If no configurations is passed, the default configuration is applied.

        Args:
            config_file_path (Optional[str], optional): _description_. Defaults to None.
        """
        
        self._avaiable_loggers = []
        self._avaiable_configs = {}
        self._avaiable_configs.setdefault(TimedLoggerDefaults.DEFAULT_CONFIG_KEY(), TimedLoggerDefaults.DEFAULT_CONFIG_VALUE())
        if config_file_path is not None:
            self.file_config(config_file_path)

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

    #ILogger methods.
    def add_logger(self, logger_name: str, configuration: Optional[str] = None) -> None:
        """
        Create a new logger with the given name.

        Args:
            logger_name (str): logger name.
            configuration (Optional[str], optional): logging configuration to be used. Defaults to None.
        """

        new_logger = getLogger(logger_name)
        if new_logger.name not in self._avaiable_loggers: self._avaiable_loggers.append(new_logger.name)

        if configuration is None\
            or self._avaiable_configs.get(configuration) == TimedLoggerDefaults.DEFAULT_CONFIG_VALUE():
            self._apply_default_config(new_logger)
        else:
            self._apply_custom_timed_config(new_logger, self._avaiable_configs.get(configuration))

    def file_config(self, config_file_path: str) -> None:
        """
        Configure the given logger with a valid configuration file.

        Args:
            config_file_path (str): absolute path of the configuration file.
        """

        if not os_path_exists(config_file_path) or not os_path_isfile(config_file_path):
            raise FileNotFoundError

        # Reading all the configurations.
        configurations = {}
        try:
            with open(config_file_path, 'r') as config_file_sream:
                configurations = safe_load(config_file_sream)
        except Exception as e:
            print(e) 
            sys.exit()

        # Adding the configurations to the avaiable configurations.
        for k, v in configurations.items():
            self._avaiable_configs[k] = TimedRotatingFileConfig.parse_obj(v)

    def debug(self, logger_name: str, message: str) -> None:
        """
        Print a debug level log statement with the specified logger.

        Args:
            logger_name (str): the logger name to use.
            message (str): the message to log.
        """
        if logger_name in self._avaiable_loggers:
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
        if logger_name in self._avaiable_loggers:
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
        if logger_name in self._avaiable_loggers:
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
        if logger_name in self._avaiable_loggers:
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
        if logger_name in self._avaiable_loggers:
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
        new_logger.setLevel(self._log_level_mapper(TimedLoggerDefaults.DEFAULT_LOG_LEVEL()))
        handler = TimedRotatingFileHandler(TimedLoggerDefaults.DEFAULT_LOG_FILE())
        fmt = TimedLoggerDefaults.DEFAULT_LOG_FORMAT()
        handler.setFormatter(fmt)

        new_logger.addHandler(handler)

    def _apply_custom_timed_config(self, new_logger: Logger, config: TimedRotatingFileConfig) -> None:
        """
        Apply a custom configuration to the given logger.

        Args:
            new_logger (Logger): logger to configure.
            config (TimedRotatingFileConfig): logger configurations.
        """
        new_logger.setLevel(self._log_level_mapper(config.level))
        handler = TimedRotatingFileHandler(
            config.filename,
            config.when,
            config.interval,
            config.backup_count,
            config.encoding,
            config.delay,
            config.utc,
            config.atTime,
            config.errors
        )
        fmt = logging.Formatter(config.format)
        handler.setFormatter(fmt)

        new_logger.addHandler(handler)
