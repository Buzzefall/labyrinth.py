# Render text representation of game world + history of actions
import os


class Renderer:
    def __init__(self, config, world_state, cli_history):
        self.config = config
        self.world_state = world_state
        self.cli_history = cli_history

    @staticmethod
    def wrap_string(string: str, max_length: int):
        if not string[max_length - 1].isspace():
            first, second = string[0:max_length], string[max_length:]
        else:

        if len(second) > max_length:
            return first + "\n" + Renderer.wrap_string(second)
        else:
            return first + "\n" + second

    # Construct text representation of world state as list of strings
    def get_world_image(self) -> list:
        return []

    # Take some last history entries as list of strings
    def get_latest_history(self):
        n_last_entries = self.config['renderer']['render_history_entries']
        return self.cli_history[-n_last_entries:]

    # Rearrange strings with world and history states and apply padding to create final image
    def compose(self, world_image: list, world_history: list) -> str:
        max_length = self.config['world']['width'] * self.config['renderer']['width_ratio']
        world_image_padding = max_length - self.config['world']['width']
        history_image_padding =


        return ''

    def update_screen(self):
        # Prepare next frame
        world_image = self.get_world_image()
        world_history = self.get_latest_history()
        next_frame = self.compose(world_image, world_history)

        # Clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])

        # Draw next frame
        print(next_frame)