from common.base import Singleton
from core.cli import CLI
from entities.cells import Cell
from entities.enum import CellType
from entities.world import GameWorld, WorldManager
from events.events import FacedWallEvent, FacedMonolithEvent
from events.system import EventSystem


# noinspection PyAttributeOutsideInit
class CommandProcessor(Singleton):
    def init(self, config):
        self.config = config
        CLI().add_event_message('InitCommandProcessor')

    @staticmethod
    def can_move_to(destination: Cell):
        player = WorldManager().get().player

        if destination is not None:
            if destination.type == CellType.Empty:
                return True
            elif destination.type == CellType.Wall:
                EventSystem().register(FacedWallEvent(player, player.cell))
            elif destination.type == CellType.Monolith:
                EventSystem().register(FacedMonolithEvent(player, player.cell))

        return False

    @staticmethod
    def is_valid(command: str) -> bool:
        player = WorldManager().get().player

        if command == 'left':
            return CommandProcessor.can_move_to(player.cell.left)

        elif command == 'right':
            return CommandProcessor.can_move_to(player.cell.right)

        elif command == 'up':
            return CommandProcessor.can_move_to(player.cell.up)

        elif command == 'down':
            return CommandProcessor.can_move_to(player.cell.down)

        elif command == 'skip':
            pass
        elif command == 'save':
            pass
        elif command == 'load':
            pass
        elif command == 'exit':
            pass

        return True
