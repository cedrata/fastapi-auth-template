from os import environ
from os.path import join
from typing import Final

from injector import Binder, Injector, singleton
from src.services.logger.implementations.logger import TimedLogger
from src.services.logger.interfaces.i_logger import ILogger


def resolve(binder: Binder) -> None:
    """
    This method is self explanatory, aims to resolve the dependencies of classes
    and interfaces. Here the instances will be created and interfaces associated
    to implementations.


    Args:
        injector (Injector): dependency injector.
    """

    # Singletons instantiations
    logger_config_file_path = join(environ["CONFIGS_DIR"], "log", "log_dev.yaml")
    logger = TimedLogger(config_file_path=logger_config_file_path)
    binder.bind(ILogger, to=logger, scope=singleton)


CONTAINER: Final[Injector] = Injector([resolve])
