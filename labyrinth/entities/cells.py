from entities.enum import CellType


class Cell:
    def __init__(self, cell_type: CellType):
        self.type = cell_type
        self.entities = []
        self.walls = {}


class RiverCell(Cell):
    pass


class RoadCell(Cell):
    pass
