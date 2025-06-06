import json
from importlib import resources as ir

from qmines.game_parameters import GameParameters

param_file = ir.files('qmines') / 'resources' / 'game_paramss.json'
param_text = param_file.read_text()
params_dict = json.loads(param_text)
params = GameParameters(**params_dict)
print('Success')