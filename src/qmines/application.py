from PySide6.QtCore import QObject
from PySide6.QtWidgets import QLabel, QToolBar

from qmines.board.board import Board
from qmines.config import Config, read_config_from_file
from qmines.mainwindow import MainWindow


class Application(QObject):

    def __init__(self) -> None:
        self._config = read_config_from_file()
        self._board = None
        self._pause_view = QLabel('Hi there')
        self._toolbar = None
        self._new_game_dialog = None
        self._mainwindow = None
        self._set_up_game(self._config)
    
    def _set_up_game(self, config: Config) -> None:
        self._board = Board(config)
        self._toolbar = QToolBar()
        self._mainwindow = MainWindow(self._board.view, self._pause_view, self._toolbar)