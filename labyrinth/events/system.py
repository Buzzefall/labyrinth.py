from queue import Queue

from common.base import Singleton
from core.cli import CLI
from entities.base import Entity
from events.base import Event


# noinspection PyAttributeOutsideInit
class EventSystem(Singleton):
    def init(self, config):
        self.config = config
        self.events = Queue()
        self.listeners = {}
        CLI().add_event_message('InitEventSystem')

    def get_listeners(self, event: Event) -> list:
        if event.name in self.listeners:
            return self.listeners[event.name]
        else:
            self.listeners[event.name] = []
            return self.listeners[event.name]

    def add_listeners(self, event: Event, listeners: list):
        event_listeners = self.get_listeners(event)
        event_listeners += listeners

    def register(self, event: Event):
        self.events.put(event)

    def update(self):
        while not self.events.empty():
            event = self.events.get()

            listeners = self.get_listeners(event)
            for lr in listeners:
                if lr is event.target:
                    lr.receive(event)

            CLI().receive(event)

