# Nests data of game world

import json
import random

from entities.enum import CellType


class GameWorld:
    def __init__(self, config):
        self.cells = [[CellType.REGULAR.value for x in range(self.w)] for y in range(self.h)]
        self.config = config
        self.w = config['width']
        self.h = config['height']

        random.seed(42)

    # TODO: Generate Labyrinth
    def generate_map(self):
        self.cells = [[CellType.REGULAR.value for x in range(self.w)] for y in range(self.h)]

    def load_map(self, file_path):
        with open(file_path) as map_file:
            self.map = json.load(map_file)

