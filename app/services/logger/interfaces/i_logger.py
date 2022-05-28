from typing import str, bool, Optional
from zope.interface import Interface as ZInterface


from app.services.logger.enums.level import LogLevel


class ILogger(ZInterface):
    """
    Interface where basic logging behaviour is defined.

    Args:
        ZInterface (zope.interface.Interface): Interface class from zope.interface.
    """



    def add_logger(logger_name: str, configuration: Optional[str] = None) -> None:
        """
        Create a new logger with the given name, and configured if configuration
        is assigned.

        Args:
            logger_name (str): _description_
            configuration (Optional[str]): path of the configuration file. Default to None.
        """

    def file_config(logger_name: str, configuration: str) -> None:
        """
        Configure the given logger with a valid configuration file.

        Args:
            logger_name (str): name of the logger to configure.
            configuration (str): path of the configuration file.
        """

    def set_logger_level(logger_name: str, level: LogLevel) -> None:
        """
        Set the given name logger log level with the given one.

        Args:
            logger_name (str): name of the logger to change level.
            level (LogLevel): the new log level.
        """

    def set_format(format: str) -> None:
        """
        Set a new format for all the loggers.

        Args:
            logger_name (str): the new log format.
        """

    def exists(logger_name: str) -> bool:
        """
        Check if any logger matching the given name exists.

        Args:
            logger_name (str): name of the logger to search
        """