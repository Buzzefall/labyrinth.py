from queue import Queue

from entities.base import Entity
from events.base import Event


class EventSystem:
    def __init__(self):
        self.events = Queue()
        self.listeners = {}
        self.broadcast_listeners = []

    def get_listeners(self, event: Event) -> list:
        if event.name in self.listeners:
            return self.listeners[event.name]
        else:
            self.listeners[event.name] = []
            return self.listeners[event.name]

    def add_broadcast_listeners(self, listeners):
        self.broadcast_listeners += listeners

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

            for lr in self.broadcast_listeners:
                lr.receive(event)

