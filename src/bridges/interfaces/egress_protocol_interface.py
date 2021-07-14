from abc import ABC, abstractmethod
from io import StringIO
from typing import Union


class EgressProtocolInterface(ABC):
    @abstractmethod
    def build_engine(self): pass

    @abstractmethod
    def send(self, filename = None, data: Union[bytearray, StringIO] = None): pass
