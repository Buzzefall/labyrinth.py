from core.cli import CLI
from entities.cells import Cell
from entities.enum import CellType
from entities.world import GameWorld
from events.events import FacedWallEvent, FacedMonolithEvent
from events.system import EventSystem


class CommandProcessor:
    def __init__(self, world: GameWorld, eventsys: EventSystem, cli: CLI):
        self.world = world
        self.eventsys = eventsys
        self.cli = cli

    def can_move_to(self, destination: Cell):
        player = self.world.player

        if destination is not None:
            if destination.type == CellType.Empty:
                return True
            elif destination.type == CellType.Wall:
                self.eventsys.register(FacedWallEvent(player, player.cell))
            elif destination.type == CellType.Monolith:
                self.eventsys.register(FacedMonolithEvent(player, player.cell))

        return False

    def is_valid(self, command: str) -> bool:
        player = self.world.player

        if command == 'left':
            return self.can_move_to(player.cell.left)

        elif command == 'right':
            return self.can_move_to(player.cell.right)

        elif command == 'up':
            return self.can_move_to(player.cell.up)

        elif command == 'down':
            return self.can_move_to(player.cell.down)

        elif command == 'skip turn':
            pass
        elif command == 'save':
            pass
        elif command == 'exit':
            pass

        return True
