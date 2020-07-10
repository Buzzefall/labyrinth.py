from uuid import uuid4

from entities.base import Entity


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.id = uuid4().int
        self.components = {}
