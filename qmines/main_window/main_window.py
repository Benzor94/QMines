import json
from importlib import resources as ir

from PySide6.QtWidgets import QMainWindow

from qmines.board.board import Board
from qmines.control_elements.mine_counter import MineCounter
from qmines.control_elements.pause_button import PauseButton
from qmines.control_elements.time_tracker import TimeTracker
from qmines.game_parameters import GameParameters, DEFAULT_PARAMS


class MainWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self._parameters: GameParameters | None = None
        self._game_board: Board | None = None
        self._mine_counter: MineCounter | None = None
        self._time_tracker: TimeTracker | None = None
        self._pause_button: PauseButton | None = None
    
    def _set_up(self, parameters: GameParameters) -> None:
        ... # See the outer mainwindow.py for outline, should complete the rest of the elements first.

    @staticmethod
    def _get_initial_parameters() -> GameParameters:
        try:
            param_file = ir.files('qmines') / 'resources' / 'game_params.json'
            param_text = param_file.read_text()
            params_dict = json.loads(param_text)
            return GameParameters(**params_dict)
        except Exception as e:
            print(f'Using default parameters. Saved parameters could not be loaded: {e}')
        return GameParameters(**DEFAULT_PARAMS)

