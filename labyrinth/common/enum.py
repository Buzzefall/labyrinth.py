from enum import Enum, unique


@unique
class CellType(Enum):
    Empty = 1
    Wall = 2
    Monolith = 3


@unique
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    @staticmethod
    def all():
        return [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]


@unique
class EntityTypes(Enum):
    NONE = 0
    PLAYER = 1
    BEAR = 2
    HEALTH = 3
    PISTOL = 4
    WORMHOLE = 5
    RIVER = 6
    BUILDING = 7
    TREASURE = 8
    EXIT = 9
