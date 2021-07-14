from abc import ABC, abstractmethod


class IOInterface(ABC):
    @abstractmethod
    def convert(self):
        pass