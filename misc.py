from typing import Optional

from pydantic import BaseModel
from zope.interface import Attribute, Interface, implementer

from app.services.logger.implementations import logger


class Mod(BaseModel):
    a: str
    b: Optional[str]

def new_meth(para: Optional[str] = None) -> None:
    print(para)


class IFoo(Interface):
    a = Attribute("attribute a")

@implementer(IFoo)
class Foo(object):

    def __init__(self, a):
        self._a = a

    @property
    def a(self):
        return self._a


if __name__=="__main__":
    # i: IFoo = Foo(4)
    # print(i.a)

    # new_meth('a')

    # mod_a: Mod = Mod()

    # print(json.dumps(mod_a, indent=2, default=pydantic_encoder))

    logger_instance = logger.CdrtLogger("./custom_log.yaml")
    print("ciao")
