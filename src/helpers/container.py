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
    logg = TimedLogger()
    binder.bind(ILogger, to=logg, scope=singleton)

CONTAINER: Final[Injector] = Injector([resolve])