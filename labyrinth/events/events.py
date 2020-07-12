from typing import Union

from entities.base import Entity
from events.base import Event


class LeftCellEvent(Event):
    def __init__(self, source: Union[Entity, None], target: Union[Entity, None]):
        super().__init__(source, target)


class EnteredCellEvent(Event):
    def __init__(self, source: Union[Entity, None], target: Union[Entity, None]):
        super().__init__(source, target)


class SkipTurnEvent(Event):
    def __init__(self, source: Union[Entity, None], target: Union[Entity, None]):
        super().__init__(source, target)


class FacedMonolithEvent(Event):
    def __init__(self, source: Union[Entity, None], target: Union[Entity, None]):
        super().__init__(source, target)


class FacedWallEvent(Event):
    def __init__(self, source: Union[Entity, None], target: Union[Entity, None]):
        super().__init__(source, target)
