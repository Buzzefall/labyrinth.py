from uuid import uuid4

from base import Entity

class Player(Entity):
    def __init__(self):
        self.id = uuid4().int
        self.components = {}
