import json
from collections.abc import Mapping

from qmines.game_parameters.game_parameters import GameParameters
from qmines.constants import DEFAULT_SETTINGS, SETTINGS_FILE

def read_settings() -> GameParameters:
    parameters_dict: Mapping[str, int] = {}
    try:
        parameters_dict = json.loads(SETTINGS_FILE.read_text())
    except Exception:
        parameters_dict = DEFAULT_SETTINGS
    return GameParameters(**parameters_dict)