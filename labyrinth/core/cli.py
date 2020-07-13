import os

from common.base import Singleton
from events.base import Listener, Event
from events.events import EnteredCellEvent, LeftCellEvent, FacedWallEvent, FacedMonolithEvent


# noinspection PyAttributeOutsideInit
class CLI(Singleton, Listener):
    msg_prefixes = {
        'player': 'Player >>> ',
        'debug': 'DEBUG  >>> ',
        'game': 'Game   >>> ',
    }

    def init(self, config):
        self.config = config
        self.history = []
        self.player_history = []
        self.debug_history = []
        self.add_event_message('InitCLI')

    def get_player_input(self, input_type: str):
        player_input = input("Enter: ").lower()
        new_entry = CLI.msg_prefixes['player'] + player_input

        self.history.append(new_entry)
        self.player_history.append(new_entry)

        if input_type == 'command':
            if player_input in self.config['cli']['commands']:
                return player_input
            else:
                self.add_event_message('wrong_command', 'Try again.')
                return None

        elif input_type == 'dimensions':
            numbers = player_input.split()
            try:
                if len(numbers) != 2:
                    raise ValueError

                numbers = int(numbers[0]), int(numbers[1])
                if numbers[0] < 4 or numbers[0] > 10 or numbers[1] < 4 or numbers[1] > 10:
                    self.add_event_message('wrong_dimensions')
                    return None

                return numbers

            except ValueError:
                self.add_event_message('wrong_input', 'What are you doing??')
                return None

    def add_event_message(self, event_name: str, message: str = ''):
        self.history.append(CLI.msg_prefixes['game'] + self.config['cli']['messages'][event_name] + message)

    def add_message(self, message: str):
        self.history.append(CLI.msg_prefixes['game'] + message)

    def receive(self, event: Event):
        if event.name not in (LeftCellEvent.__name__, ):
            self.add_event_message(event.name, f'Location: ({event.target.x}, {event.target.y})')

    def debug(self, string):
        message = CLI.msg_prefixes['debug'] + string
        self.history.append(message)
        self.debug_history.append(message)

