from enum import Enum, unique


@unique
class CellType(Enum):
    MONOLITH = -1,
    REGULAR = 0,


@unique
class EntityTypes(Enum):
    MONOLITH = -1
    CELL = 0

    PLAYER = 1
    TREASURE = 2
    KNIFE = 3
    PISTOL = 4
    HEALTH = 5
    BEAR = 6
    WORMHOLE = 7
    RIVER = 8
    BUILDING = 9
