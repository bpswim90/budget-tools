import pathlib
import json

root_dir = pathlib.Path().parent.parent
config_path = root_dir / 'budgetConfig.json'


def load_config():
    """Load in config json file"""
    with open(config_path, 'r', encoding="utf-8") as f:
        return json.load(f)
