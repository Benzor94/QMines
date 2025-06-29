import json
from importlib.resources import as_file

from qmines.game_parameters.game_parameters import GameParameters
from qmines.utilities.constants import EASY_SETTINGS, SETTINGS_FILE

def read_settings() -> GameParameters:
    try:
        parameters_dict = json.loads(SETTINGS_FILE.read_text())
        parameters = GameParameters.from_dict(parameters_dict)
    except (FileNotFoundError, ValueError, TypeError):
        parameters = GameParameters.from_dict(EASY_SETTINGS)
    return parameters

def write_settings(parameters: GameParameters) -> None:
    parameters_dict = parameters.to_dict()
    with as_file(SETTINGS_FILE) as f:
        file = f.open('w')
        json.dump(parameters_dict, file, indent=2)
        file.close()