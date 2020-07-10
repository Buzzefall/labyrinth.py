import os


class CLI:

    def __init__(self, config):
        self.config = config
        self.history = []
        self.debug_history = []

    def debug(self, string):
        message = {
            'entry_type': 'Debug',
            'message': f'DEBUG: {string}'
        }

        self.history.append(message)
        self.debug_history.append(message)

    def get_player_input(self, input_type: str) -> str:
        input_type = input_type.upper()
        try:
            assert input_type in self.config['input_types']
        except AssertionError:
            self.debug(f'Wrong player input type, assuming on of: {self.input_types}')
            return 'ERROR'

        self.history.append(f'What is your {input_type}?')
        self.render()

        player_input = input()
        player_input = player_input[0].upper() + player_input[1:]
        self.player_history[input_type].append(player_input)

        self.history.append(f'{input_type}: {player_input}')
        self.render()

        return player_input

    def get_history(self, n_lines: int):
        return self.history

    def render(self):
        os.system(['clear', 'cls'][os.name == 'nt'])
        for line in self.get_history(5):
            print(line)
