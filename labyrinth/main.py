# Entry point for the application

import os
import json
from pathlib import Path

from core.engine import Engine


if __name__ == '__main__':
    cfg_path = Path(f'{os.getcwd()}/config/config.json')
    with open(cfg_path) as config_file:
        config = json.load(config_file)

    engine = Engine(config)

    engine.run()
