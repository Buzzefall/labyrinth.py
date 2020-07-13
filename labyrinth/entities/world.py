# Nests data of game world

import random

from common.enum import CellType
from entities.player import Player
from entities.treasure import Treasure


class GameWorld:
    def __init__(self, config, cells):
        self.config = config
        self.cells = cells
        self.player = None
        self.treasure = None

        self.populate_entities()

    def populate_entities(self):
        empty_cells = [cell for row in self.cells for cell in row if cell.type == CellType.Empty]

        player_spawn = random.choice(empty_cells)
        self.player = Player('Noname', player_spawn)
        player_spawn.add_entity(self.player)
        empty_cells.remove(player_spawn)

        treasure_spawn = random.choice(empty_cells)
        self.treasure = Treasure(treasure_spawn)
        treasure_spawn.add_entity(self.treasure)
        empty_cells.remove(treasure_spawn)