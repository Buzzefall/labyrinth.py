# Nests data of game world
import os

import pickle
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Union

from common.base import Singleton
from core.cli import CLI
from entities.enum import CellType, Direction
from entities.cells import Cell
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


# noinspection PyAttributeOutsideInit
class WorldManager(Singleton):
    def init(self, config):
        random.seed()

        self.config = config
        self.width = config['world']['width']
        self.height = config['world']['height']

        CLI().add_event_message('InitWorldManager')

        self.cells = self.generate_empty()
        self.world = self.generate()

    def save(self):
        if self.world is None:
            return

        dt = datetime.today()
        save_name = f'Labyrinth - {str(dt)}.pickle'
        file = f"{os.getcwd()}/{self.config['paths']['saves']}/{save_name}"

        with open(file, 'wb') as save_file:
            recursion_limit = 0
            success = False
            while not success:
                try:
                    pickle.dump(self.cells, save_file)
                    CLI().add_message(f'Saved map with recursion limit {recursion_limit}')
                    success = True
                except RecursionError:
                    recursion_limit += 1000
                    sys.setrecursionlimit(recursion_limit)

    def load(self, save_name: Union[str, Path]):
        if not save_name:
            save_name = f'{os.getcwd()}/{self.config["paths"]["test_map"]}'

        with open(f"{os.getcwd()}/{self.config['paths']['saves']}/{save_name}") as save_file:
            self.world = pickle.load(save_file)

        return self.world

    @staticmethod
    def check_next(wall: Cell, next_cell: Cell, not_visited: list, find_visited: bool = False) -> bool:
        """ Checks the wall and if cell behind it is visited. Returns bool."""
        return wall.type == CellType.Wall and (next_cell in not_visited or find_visited)

    @staticmethod
    def find_next(cell: Cell, not_visited: list, find_visited: bool) -> (object, object):
        """ Finds visited or not visited cell adjacent to given.
            Returns tuple of (wall_between: Cell, next_cell: Cell). """
        directions = Direction.all()
        while len(directions) > 0:
            chosen_dir = random.choice(directions)
            directions.remove(chosen_dir)

            if chosen_dir == Direction.LEFT:
                if WorldManager.check_next(cell.left, cell.left.left, not_visited, find_visited):
                    return cell.left, cell.left.left

            elif chosen_dir == Direction.RIGHT:
                if WorldManager.check_next(cell.right, cell.right.right, not_visited, find_visited):
                    return cell.right, cell.right.right

            elif chosen_dir == Direction.UP:
                if WorldManager.check_next(cell.up, cell.up.up, not_visited, find_visited):
                    return cell.up, cell.up.up

            elif chosen_dir == Direction.DOWN:
                if WorldManager.check_next(cell.down, cell.down.down, not_visited, find_visited):
                    return cell.down, cell.down.down

        return None, None

    @staticmethod
    def random_walk(start: Cell, not_visited: list):
        wall, next_cell = WorldManager.find_next(start, not_visited, False)
        if wall is not None and next_cell is not None:
            wall.type = CellType.Empty
            not_visited.remove(next_cell)
            WorldManager.random_walk(next_cell, not_visited)

    @staticmethod
    def find_adjacent(not_visited: list) -> Union[Cell, None]:
        """ Finds not visited cell adjacent to visited. Returns Cell or None """
        random.shuffle(not_visited)
        for cell in not_visited:
            wall, adjacent = WorldManager.find_next(cell, not_visited, True)
            if adjacent is not None:
                wall.type = CellType.Empty
                return adjacent

        return None

    @staticmethod
    def hunt_and_kill(not_visited: list):
        start_cell = WorldManager.find_adjacent(not_visited)
        if start_cell is not None:
            WorldManager.random_walk(start_cell, not_visited)
            WorldManager.hunt_and_kill(not_visited)

    @staticmethod
    def explode(center: Cell, radius: int, affected: list = []):
        if radius <= 0:
            return

        if center.left is not None and center.left not in affected:
            if center.left.type == CellType.Wall:
                center.left.type = CellType.Empty

            affected.append(center.left)
            WorldManager.explode(center.left, radius - 1, affected)

        if center.right is not None and center.right not in affected:
            if center.right.type == CellType.Wall:
                center.right.type = CellType.Empty

            affected.append(center.right)
            WorldManager.explode(center.right, radius - 1, affected)

        if center.up is not None and center.up not in affected:
            if center.up.type == CellType.Wall:
                center.up.type = CellType.Empty

            affected.append(center.up)
            WorldManager.explode(center.up, radius - 1, affected)

        if center.down is not None and center.down not in affected:
            if center.down.type == CellType.Wall:
                center.down.type = CellType.Empty

            affected.append(center.down)
            WorldManager.explode(center.down, radius - 1, affected)

    def generate_empty(self):
        h_cells = 2 * self.width + 1
        v_cells = 2 * self.height + 1

        cells = []
        for y in range(v_cells):
            cells.append([])
            for x in range(h_cells):
                if x == 0 or x == (h_cells - 1) or y == 0 or y == (v_cells - 1):
                    cells[y].append(Cell(CellType.Monolith, x, y))
                elif x % 2 == 1 and y % 2 == 1:
                    cells[y].append(Cell(CellType.Empty, x, y))
                else:
                    cells[y].append(Cell(CellType.Wall, x, y))

        for y in range(v_cells):
            for x in range(h_cells):
                neighbours = {
                    'left': cells[y][x - 1] if x > 0 else None,
                    'right': cells[y][x + 1] if x + 1 < h_cells else None,
                    'up': cells[y - 1][x] if y > 0 else None,
                    'down': cells[y + 1][x] if y + 1 < v_cells else None
                }
                cells[y][x].add_neighbours(neighbours)

        return cells

    # noinspection PyTypeChecker
    def generate(self) -> GameWorld:
        random.seed()

        cells = self.generate_empty()

        not_visited = [cell for row in cells for cell in row if cell.type == CellType.Empty]
        WorldManager.random_walk(random.choice(not_visited), not_visited)
        WorldManager.hunt_and_kill(not_visited)

        for k in range(len(cells) // 5):
            x = random.randint(0, len(cells[0]) - 1)
            y = random.randint(0, len(cells) - 1)
            WorldManager.explode(cells[y][x], random.randint(1, len(cells)) // 2)

        self.world = GameWorld(self.config, cells)
        return self.world

    def get(self):
        if self.world is not None:
            return self.world
        else:
            self.world = self.generate()
            return self.world
