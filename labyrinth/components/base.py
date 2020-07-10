from uuid import uuid4


# Base class for all components
class Component(object):
    def __init__(self):
        self.id = uuid4().int

    def update(self):
        pass
