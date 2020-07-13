from entities.enum import CellType
from entities.base import Entity

from events.base import Listener, Event
from events.events import EnteredCellEvent, LeftCellEvent


class Cell(Entity, Listener):
    def __init__(self, cell_type: CellType, x: int, y: int):
        super().__init__()
        self.type = cell_type
        self.visible = True
        self.x = x
        self.y = y
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.entities = []

    def add_neighbours(self, neighbours: dict):
        self.up = neighbours['up'] if 'up' in neighbours else None
        self.down = neighbours['down'] if 'down' in neighbours else None
        self.left = neighbours['left'] if 'left' in neighbours else None
        self.right = neighbours['right'] if 'right' in neighbours else None

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def remove_entity(self, entity: Entity):
        self.entities.remove(entity)

    def find_player(self):
        def is_player(obj):
            return type(obj).__name__ == 'Player'

        for e in self.entities:
            if is_player(e):
                return e

        return None

    def find_treasure(self):
        def is_treasure(obj):
            return type(obj).__name__ == 'Treasure'

        for e in self.entities:
            if is_treasure(e):
                return e

        return None

    def reveal(self):
        l, r, u, p = self.left, self.right, self.up, self.down
        self.visible = True

        for neighbour in (l, r, u, p, l.up, l.down, r.up, r.down):
            neighbour.visible = True

    def receive(self, event: Event):
        if isinstance(event, EnteredCellEvent):
            player = event.source
            self.add_entity(player)

            treasure = self.find_treasure()
            if treasure is not None:
                player.inventory.add(treasure)
                self.entities.remove(treasure)

            self.reveal()
        elif isinstance(event, LeftCellEvent):
            self.remove_entity(event.source)

    def __str__(self):
        if self.find_player():
            return '℗ '
        elif self.find_treasure():
            return '⌛'
        elif not self.visible or self.type == CellType.Empty:
            return '  '
        elif self.type == CellType.Monolith:
            return '▧ '
        elif self.type == CellType.Wall:
            return '# '

#  ҉
