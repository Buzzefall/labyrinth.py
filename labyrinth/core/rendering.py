# Render text representation of game world + history of actions
import os

from common.base import Singleton
from common.utils import wrap_string

from core.cli import CLI
from entities.world import GameWorld
from core.manager import WorldManager


class TextTile:
    def __init__(self, rows: list, max_width: int = 0, padding: int = 0):
        if padding > 0:
            self.rows = [(' ' * padding) + row for row in rows]
        else:
            self.rows = rows

        if padding == 0 and max_width > max(len(row) for row in rows):
            self.text = "\n".join(wrap_string(row, max_width) for row in self.rows)
        else:
            self.text = "\n".join(self.rows)

        self.width = max_width

    def __str__(self):
        return self.text

    def __add__(self, other):
        rows = [str(self), "\n", str(other)]
        return TextTile(rows, max_width=max(self.width, other.width))


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic
class Renderer(Singleton):
    def init(self, config: dict):
        self.config = config
        CLI().add_event_message('InitRenderer')

    def get_world_image(self) -> list:
        return [''.join(str(cell) for cell in row) for row in WorldManager().get().cells]

    # Take some last history entries as list of strings
    def get_history(self):
        total = len(CLI().history)
        n_last = self.config['renderer']['cli_history_trail']
        history_slice = CLI().history[-n_last:]

        start_idx = total - n_last if total - n_last > 0 else 0
        return [f"[{start_idx + 1 + i}]\t" + entry for i, entry in enumerate(history_slice)]

    def compose(self, world_image: list, cli_history: list) -> str:
        maze_width = 2 * self.config['world']['width'] + 1
        max_width = maze_width * self.config['renderer']['width_ratio']
        world_image_padding = round((max_width - maze_width) / 2)

        world_tile = TextTile(world_image, max_width, world_image_padding)
        history_tile = TextTile(cli_history, max_width)
        composite_tile = world_tile + history_tile

        return str(composite_tile)

    def update_screen(self):
        # Prepare next frame
        world_image = self.get_world_image()
        cli_history = self.get_history()
        next_frame = self.compose(world_image, cli_history)

        # Clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])

        # Draw next frame
        print(next_frame)
