from components.base import Component


class InputComponent(Component):
    def __init__(self, source):
        super().__init__()
        self.source = source
        self.state = None


class PlayerInputComponent(InputComponent):
    def __init__(self, source):
        super().__init__(source)

    def update_state(self):
        self.state = self.source.get_input()
