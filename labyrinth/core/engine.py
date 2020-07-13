from common.base import Singleton

from core.cli import CLI
from core.processor import CommandProcessor
from core.rendering import Renderer

from common.enum import Direction, CellType
from core.manager import WorldManager

from events.system import EventSystem
from events.events import EnteredCellEvent, LeftCellEvent, SkipTurnEvent, FacedWallEvent, FacedMonolithEvent, \
    TreasureFoundEvent


# Load CLI. Initialize. Run game-loop.
# noinspection PyAttributeOutsideInit
class Engine(Singleton):
    def init(self, config):
        self.config = config

        CLI().init(config)
        WorldManager().init(config)
        Renderer().init(config)
        CommandProcessor().init(config)
        EventSystem().init(config)

        CLI().add_message('Finished initialization.')

    def make_new_world(self):
        self.init(self.config)
        WorldManager().generate()
        Engine.register_listeners()
        CLI().add_event_message('WorldCreated')

    @staticmethod
    def register_listeners():
        world = WorldManager().get()

        traversable_cells = [cell for row in world.cells for cell in row if cell.type == CellType.Empty]
        EventSystem().add_listeners(EnteredCellEvent(), traversable_cells)
        EventSystem().add_listeners(LeftCellEvent(), traversable_cells)
        EventSystem().add_listeners(TreasureFoundEvent(), traversable_cells)

        # EventSystem().add_listeners(FacedWallEvent(), [])
        # EventSystem().add_listeners(FacedMonolithEvent(), [])
        # EventSystem().add_listeners(SkipTurnEvent(), [])

    @staticmethod
    def save_world():
        WorldManager().save()

    @staticmethod
    def load_save():
        WorldManager().load()
        Engine.register_listeners()

    def run(self):
        WorldManager().generate()
        Engine.register_listeners()
        CLI().add_message('Good day, Player! Welcome to Labyrinth')

        dimensions = None
        while dimensions is None:
            CLI().add_event_message('choose_dimensions')
            Renderer().update_screen()
            dimensions = CLI().get_player_input('dimensions')

        self.config['world']['width'] = dimensions[0]
        self.config['world']['height'] = dimensions[1]

        self.make_new_world()

        CLI().add_event_message('choose_command', 'Enter commands!')

        game_over = False
        while not game_over:
            command = None
            while command is None:
                Renderer().update_screen()
                command = CLI().get_player_input('command')

            if CommandProcessor().is_valid(command):
                Engine.execute(command)

            if command == 'exit':
                game_over = True

            EventSystem().update()
            Renderer().update_screen()

    @staticmethod
    def execute(command: str):
        player = WorldManager().get().player
        eventsys = EventSystem()

        if command == 'left':
            eventsys.register(LeftCellEvent(player, player.cell))
            player.move(Direction.LEFT)
            eventsys.register(EnteredCellEvent(player, player.cell))

        elif command == 'right':
            eventsys.register(LeftCellEvent(player, player.cell))
            player.move(Direction.RIGHT)
            eventsys.register(EnteredCellEvent(player, player.cell))

        elif command == 'up':
            eventsys.register(LeftCellEvent(player, player.cell))
            player.move(Direction.UP)
            eventsys.register(EnteredCellEvent(player, player.cell))

        elif command == 'down':
            eventsys.register(LeftCellEvent(player, player.cell))
            player.move(Direction.DOWN)
            eventsys.register(EnteredCellEvent(player, player.cell))

        elif command == 'skip':
            eventsys.register(SkipTurnEvent(player, player.cell))

        elif command == 'save':
            Engine.save_world()

        elif command == 'load':
            Engine.load_save()

        elif command == 'exit':
            return
