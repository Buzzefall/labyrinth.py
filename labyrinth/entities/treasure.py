from entities.base import Entity
from events.base import Listener, Event
from events.events import EnteredCellEvent


class Treasure(Entity, Listener):
    def __init__(self):
        super().__init__()

    def receive(self, event: Event):
        if isinstance(event, EnteredCellEvent):
            event.source.inventory.add(self)
