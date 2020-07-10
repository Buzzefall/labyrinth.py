# Nests data of game world

import json
import random

from core.cells import CellTypes


class GameWorld:
    def __init__(self, config):
        self.cells = [[CellTypes.REGULAR.value for x in range(self.w)] for y in range(self.h)]
        self.config = config
        self.w = config['width']
        self.h = config['height']

        random.seed(42)

    def generate_map(self):
        self.cells = [[CellTypes.REGULAR.value for x in range(self.w)] for y in range(self.h)]

    def load_map(self, file_path):
        with open(file_path) as map_file:
            self.map = json.load(map_file)

