import json

from qmines.game_parameters.game_parameters import GameParameters
from qmines.constants import DEFAULT_SETTINGS, SETTINGS_FILE

def read_settings() -> GameParameters:
    try:
        parameters_dict = json.loads(SETTINGS_FILE.read_text())
        parameters = GameParameters(**parameters_dict)
    except (FileNotFoundError, ValueError, TypeError):
        parameters = GameParameters(**DEFAULT_SETTINGS)
    return parameters