# Render text representation of game world + history of actions
import os

from common.utils import wrap_string

from core.cli import CLI
from entities.world import GameWorld


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


class Renderer:
    def __init__(self, config, world: GameWorld, cli: CLI):
        self.config = config
        self.cli = cli
        # world.history будет хранить отдельную свою историю
        # и её можно рисовать отдельным тайлом
        self.world = world

    # TODO: Construct text representation of world state as list of strings
    def get_world_image(self) -> list:
        return [''.join(str(cell) for cell in row) for row in self.world.cells]

    # Take some last history entries as list of strings
    def get_cli_history(self):
        total = len(self.cli.history)
        n_last = self.config['renderer']['cli_history_trail']
        history_slice = self.cli.history[-n_last:]

        start_idx = total - n_last if total - n_last > 0 else 0
        return [f"[{start_idx + 1 + i}]\t" + entry for i, entry in enumerate(history_slice)]

    # TODO: Rearrange strings with world and history states and apply padding to create final image
    def compose(self, world_image: list, cli_history: list) -> str:
        maze_width = 2 * self.config['world']['width'] + 1
        max_width = maze_width * self.config['renderer']['width_ratio']
        world_image_padding = round((max_width - maze_width) / 2)

        world_tile = TextTile(world_image, max_width, world_image_padding)
        history_tile = TextTile(cli_history, max_width)

        return str(world_tile + history_tile)

    def update_screen(self):
        # Prepare next frame
        world_image = self.get_world_image()
        cli_history = self.get_cli_history()
        next_frame = self.compose(world_image, cli_history)

        # Clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])

        # Draw next frame
        print(next_frame)
