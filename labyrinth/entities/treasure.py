from entities.base import Entity
from entities.cells import Cell
from events.base import Event
from events.events import EnteredCellEvent


class Treasure(Entity):
    def __init__(self, cell: Cell):
        super().__init__()
        self.cell = cell

    def receive(self, event: Event):
        if isinstance(event, EnteredCellEvent):
            event.source.inventory.add(Treasure(self.cell))
            del self
