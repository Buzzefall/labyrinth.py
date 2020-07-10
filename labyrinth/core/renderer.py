# Render text representation of game world + history of actions
import os


class Helper:
    @staticmethod
    def wrap_string(string: str, max_length: int):
        if not string[max_length - 1].isspace():
            break_point = string[:max_length].rfind(' ')
            first, second = string[:break_point + 1], string[break_point + 1:]
        else:
            first, second = string[:max_length], string[max_length:]

        if len(second) > max_length:
            return first + "\n" + Helper.wrap_string(second)
        else:
            return first + "\n" + second


class Renderer:
    def __init__(self, config, world_state, cli_history):
        self.config = config
        self.cli_history = cli_history
        # world_state будет хранить отдельную свою историю
        # и её можно рисовать отдельным тайлом
        self.world_state = world_state

    # TODO: Construct text representation of world state as list of strings
    def get_world_image(self) -> list:
        return []

    # Take some last history entries as list of strings
    def get_cli_history(self):
        n_last_entries = self.config['renderer']['cli_history_trail']
        return self.cli_history[-n_last_entries:]

    def get_world_history(self):
        n_last_entries = self.config['renderer']['world_history_trail']
        return self.world_state.events[-n_last_entries:]

    # TODO: Rearrange strings with world and history states and apply padding to create final image
    def compose(self, world_image: list, cli_history: list) -> str:
        max_length = (2 + self.config['world']['width']) * self.config['renderer']['width_ratio']
        world_image_padding = round(max_length - (2 + self.config['world']['width']) / 2)
        list(map(Helper.wrap_string, cli_history))

        return ''

    def update_screen(self):
        # Prepare next frame
        world_image = self.get_world_image()
        cli_history = self.get_cli_history()
        # world_history = self.get_world_history()

        next_frame = self.compose(world_image, cli_history)

        # Clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])

        # Draw next frame
        print(next_frame)
