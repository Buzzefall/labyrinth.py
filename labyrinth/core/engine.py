from common.utils import getchar
from core.cli import CLI
from core.rendering import Renderer
from core.processor import CommandProcessor

from entities.world import GameWorld, WorldManager
from entities.enum import Direction, CellType

from events.system import EventSystem
from events.events import EnteredCellEvent, LeftCellEvent, SkipTurnEvent, FacedWallEvent, FacedMonolithEvent


# Load CLI. Initialize. Run game-loop.
class Engine:
    def __init__(self, config):
        self.config = config

        self.worldman = WorldManager(config)
        self.world = self.worldman.generate()

        self.cli = CLI(config)
        self.renderer = Renderer(config, self.world, self.cli)
        self.eventsys = EventSystem()
        self.processor = CommandProcessor(self.world, self.eventsys, self.cli)

        self.register_listeners()

    def make_new_world(self):
        self.worldman = WorldManager(self.config)
        self.world = self.worldman.generate()

        self.renderer = Renderer(self.config, self.world, self.cli)
        self.eventsys = EventSystem()
        self.processor = CommandProcessor(self.world, self.eventsys, self.cli)

        self.register_listeners()
        self.cli.add_event_message('WorldCreated')

    def register_listeners(self):
        traversable_cells = [cell for row in self.world.cells for cell in row if cell.type == CellType.Empty]
        self.eventsys.add_listeners(EnteredCellEvent(None, None), traversable_cells)
        self.eventsys.add_listeners(LeftCellEvent(None, None), traversable_cells)

        self.eventsys.add_broadcast_listeners([self.cli])

        self.eventsys.add_listeners(FacedWallEvent(None, None), [])
        self.eventsys.add_listeners(FacedMonolithEvent(None, None), [])

    def save_the_world(self):
        self.worldman.save()

    def run(self):
        self.cli.add_message('Good day, Player!')

        dimensions = None
        while dimensions is None:
            self.cli.add_event_message('choose_dimensions')
            self.renderer.update_screen()
            dimensions = self.cli.get_player_input('dimensions')

        self.config['world']['width'] = dimensions[0]
        self.config['world']['height'] = dimensions[1]

        self.make_new_world()

        self.cli.add_event_message('choose_command', 'Enter commands!')

        game_over = False
        while not game_over:
            command = None
            while command is None:
                self.renderer.update_screen()
                command = self.cli.get_player_input('command')

            if self.processor.is_valid(command):
                self.execute(command)

            if command == 'exit':
                game_over = True

            self.eventsys.update()
            self.renderer.update_screen()

    def execute(self, command: str):
        player = self.world.player

        if command == 'left':
            self.eventsys.register(LeftCellEvent(player, player.cell))
            player.move(Direction.LEFT)
            self.eventsys.register(EnteredCellEvent(player, player.cell))
            # self.cli.add_event_message('move', f'({player.cell.x}, {player.cell.y})')

        elif command == 'right':
            self.eventsys.register(LeftCellEvent(player, player.cell))
            player.move(Direction.RIGHT)
            self.eventsys.register(EnteredCellEvent(player, player.cell))
            # self.cli.add_event_message('move', f'({player.cell.x}, {player.cell.y})')

        elif command == 'up':
            self.eventsys.register(LeftCellEvent(player, player.cell))
            player.move(Direction.UP)
            self.eventsys.register(EnteredCellEvent(player, player.cell))
            # self.cli.add_event_message('move', f'({player.cell.x}, {player.cell.y})')

        elif command == 'down':
            self.eventsys.register(LeftCellEvent(player, player.cell))
            player.move(Direction.DOWN)
            self.eventsys.register(EnteredCellEvent(player, player.cell))
            # self.cli.add_event_message('move', f'({player.cell.x}, {player.cell.y})')

        elif command == 'save':
            self.save_the_world()
        elif command == 'skip turn':
            self.eventsys.register(SkipTurnEvent(player, player.cell))
        elif command == 'exit':
            return
