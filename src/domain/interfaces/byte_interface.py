from abc import ABC, abstractmethod


class ByteInterface(ABC):
    @abstractmethod
    def convert(self):
        pass