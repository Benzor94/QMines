from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QLabel

from qmines.board.board import Board
from qmines.config import Config, read_config_from_file
from qmines.enums import GameOverReason, TimerStateChange
from qmines.mainwindow import MainWindow
from qmines.toolbar.toolbar import Toolbar


class Application(QObject):
    time_tracking_state_change = Signal(TimerStateChange)

    def __init__(self) -> None:
        super().__init__()
        self._config = read_config_from_file()
        self._board = None
        self._pause_view = QLabel('Hi there')
        self._toolbar = None
        self._new_game_dialog = None
        self._mainwindow = None
        self._set_up_game(self._config)

    @Slot()
    def on_game_start(self) -> None:
        self.time_tracking_state_change.emit(TimerStateChange.START)

    @Slot(GameOverReason)
    def on_game_over(self) -> None:
        self.time_tracking_state_change.emit(TimerStateChange.STOP)

    def _set_up_game(self, config: Config) -> None:
        self._board = Board(config)
        self._toolbar = Toolbar(self._config)
        self._mainwindow = MainWindow(self._board.view, self._pause_view, self._toolbar.view)
        # Connections
        self._board.game_started.connect(self.on_game_start)
        self._board.game_over.connect(self.on_game_over)
        self._board.flag_changed.connect(self._toolbar.on_flag_count_change)
        self.time_tracking_state_change.connect(self._toolbar.on_time_tracking_state_change)
