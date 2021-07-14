from abc import ABC, abstractmethod
from io import StringIO
from typing import Union

from src.bridges.interfaces.egress_protocol_interface import EgressProtocolInterface


class EgressBridge(ABC):
    @abstractmethod
    def send(self):
        pass


class EgressData(EgressBridge):
    def __init__(self, filename, data: Union[bytes, StringIO], protocol: EgressProtocolInterface):
        self.protocol = protocol
        self.filename = filename
        self.data = data

    def send(self):
        self.protocol.send(self.filename, self.data)

