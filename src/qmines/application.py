from PySide6.QtCore import QObject

from qmines.config import Config, read_config_from_file
from qmines.mainwindow import MainWindow


class Application(QObject):

    def __init__(self) -> None:
        self._config = read_config_from_file()
        self._board = None
        self._toolbar = None
        self._new_game_dialog = None
        self._mainwindow = None
    
    def _set_up_game(self, config: Config) -> None:
        ...