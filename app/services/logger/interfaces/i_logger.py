from typing import str, bool, Optional
from zope.interface import Interface as ZInterface


from app.services.logger.enums.level import LogLevel


class ILogger(ZInterface):
    """
    Interface where basic logging behaviour is defined.

    Args:
        ZInterface (zope.interface.Interface): Interface class from zope.interface.
    """

    def add_logger(logger_name: str) -> None:
        """
        Create a new logger with the given name.

        Args:
            logger_name (str): logger name.
        """

    def file_config(config_file_path: str) -> None:
        """
        Configure the given logger with a valid configuration file.

        Args:
            config_file_path (str): absolute path of the configuration file.
        """

    def print_log(logger_name: str, logger_level: LogLevel, message: str) -> None:
        """
        Print a log statement with the specified logger with the given level.

        Args:
            logger_name (str): the logger name to use.
            logger_level (str): the log level to print.
            message (str): the message to log.
        """