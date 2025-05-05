

from PySide6.QtWidgets import QMainWindow

from qmines.game_parameters import GameParameters


class MainWindow(QMainWindow):
    
    def __init__(self, parameters: GameParameters) -> None:
        super().__init__()
        self._parameters = parameters
        self._game_board = None
        self._mine_counter = None
        self._time_tracker = None
        self._pause_button = None
    
    def _set_up(self) -> None:
        ... # See the outer mainwindow.py for outline, should complete the rest of the elements first.

