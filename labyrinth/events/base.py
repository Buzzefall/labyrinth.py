from abc import abstractmethod, ABC
from typing import Union

from entities.base import Entity


class Event(ABC):
    def __init__(self, source: Union[Entity, None] = None, target: Union[Entity, None] = None, data=None):
        self.source = source
        self.target = target
        self.data = data
        self.name = type(self).__name__


class Listener:
    @abstractmethod
    def receive(self, event: Event):
        pass
