from abc import abstractmethod

from entities.base import Entity


class Event:
    def __init__(self, source: Entity, target: Entity):
        self.source = source
        self.target = target
        self.name = type(self).__name__


class Listener:
    @abstractmethod
    def receive(self, event: Event):
        pass
