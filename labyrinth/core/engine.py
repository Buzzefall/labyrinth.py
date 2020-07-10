from entities.world import GameWorld
from core.cli import CLI
from core.renderer import Renderer


# Load CLI. Initialize. Run game-loop.
class Engine:
    def __init__(self, config):
        self.config = config
        self.cli = CLI(config['cli'])
        self.world = GameWorld(config['world'])
        self.renderer = Renderer(config, self.world, self.cli.get_history())

    def run(self):
        action = ''
        # while action != 'stop':
        #     action = self.cli.get_player_input('action')
        #     choice = self.cli.get_player_input('choice')
        #     history = self.cli.get_history(5)

    def update(self):
        pass
