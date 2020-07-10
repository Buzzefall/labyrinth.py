# Nests data of game world


from entities.cells import Cell
import random


class GameWorld:
    def __init__(self, config):
        random.seed(42)

        w = config['width']
        h = config['height']

        self.cells = [[Cell(random.randint(0, 10)) for y in range(h)] for x in range(w)]

    def load_map(self, path):
