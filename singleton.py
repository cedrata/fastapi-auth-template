from app.core.di.containers import Container

from dependency_injector.wiring import Provide, inject

from app.services.logger.interfaces.i_logger import ILogger

@inject
def main(logger: ILogger = Provide[Container.log_service]) -> None:
    logger.add_logger('main', 'hard_log')
    logger.info('main', 'INFO LOG')
    logger.critical('main', 'CRITICAL LOG')

if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    
    main()