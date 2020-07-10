from enum import Enum, unique


@unique
class CellType(Enum):
    MONOLITH = -1,
    REGULAR = 0,


@unique
class EntityTypes(Enum):
    PLAYER = 0
    TREASURE = 1
    KNIFE = 2
    PISTOL = 3
    HEALTH = 4
    BEAR = 5
    WORMHOLE = 6
    RIVER = 7
    BUILDING = 8
