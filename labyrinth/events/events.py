from typing import Union

from entities.base import Entity
from events.base import Event


class LeftCellEvent(Event):
    def __init__(self, source: Union[Entity, None] = None, target: Union[Entity, None] = None, data=None):
        super().__init__(source, target, data)


class EnteredCellEvent(Event):
    def __init__(self, source: Union[Entity, None] = None, target: Union[Entity, None] = None, data=None):
        super().__init__(source, target, data)


class SkipTurnEvent(Event):
    def __init__(self, source: Union[Entity, None] = None, target: Union[Entity, None] = None, data=None):
        super().__init__(source, target, data)


class FacedMonolithEvent(Event):
    def __init__(self, source: Union[Entity, None] = None, target: Union[Entity, None] = None, data=None):
        super().__init__(source, target, data)


class FacedWallEvent(Event):
    def __init__(self, source: Union[Entity, None] = None, target: Union[Entity, None] = None, data=None):
        super().__init__(source, target, data)


class TreasureFoundEvent(Event):
    def __init__(self, source: Union[Entity, None] = None, target: Union[Entity, None] = None, data=None):
        super().__init__(source, target, data)
