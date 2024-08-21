import pathlib
import json

root_dir = pathlib.Path().parent.parent
configPath = root_dir / 'budgetConfig.json'


def loadConfig():
    """Load in config json file"""
    with open(configPath, 'r') as f:
        return json.load(f)
