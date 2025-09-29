from PySide6.QtCore import QObject
from PySide6.QtWidgets import QLabel, QPushButton, QToolBar

from qmines.board.board import Board
from qmines.config import Config, read_config_from_file
from qmines.mainwindow import MainWindow
from qmines.toolbar.actions import NewGameAction, PauseAction
from qmines.toolbar.counters import MineCounter, TimeTracker
from qmines.toolbar.toolbar_view import ToolbarView


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
        self._toolbar = ToolbarView(NewGameAction(), PauseAction(), MineCounter(10), TimeTracker())
        self._mainwindow = MainWindow(self._board.view, self._pause_view, self._toolbar)