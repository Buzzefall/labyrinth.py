from uuid import uuid4

class Entity:
    def __init__(self):
        self.id = uuid4().int
        self.components = {}

    def add_component(self, component):
        pass

    def remove_component(self, component_id):
        pass

    def get_component(self, name):
        pass