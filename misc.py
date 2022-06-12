import logging
from typing import Optional

from pydantic import BaseModel

from app.services.logger.implementations import logger
from app.services.logger.interfaces.i_logger import ILogger


class Mod(BaseModel):
    a: str
    b: Optional[str]

def new_meth(para: Optional[str] = None) -> None:
    print(para)

def pippo(lg: ILogger):
    lg.critical('hard_log', 'from function pippo')

if __name__=="__main__":
    # i: IFoo = Foo(4)
    # print(i.a)

    # new_meth('a')

    # mod_a: Mod = Mod()

    # print(json.dumps(mod_a, indent=2, default=pydantic_encoder))

    logger_instance = logger.TimedLogger("./custom_log.yaml")
    # logger_instance = logger.CdrtLogger()
    logger_instance.add_logger(logger_name="pippo")
    logger_instance.info("pippo", "A simple log")
    logger_instance.add_logger(logger_name="hard_log", configuration="hard_log")
    logger_instance.critical("hard_log", "critical message")
    pippo(logger_instance)