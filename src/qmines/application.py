from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QLabel

from qmines.board.board import Board
from qmines.config import Config, read_config_from_file, write_config_to_file
from qmines.enums import GameOverReason, PauseAvailability, TimerStateChange
from qmines.mainwindow import MainWindow
from qmines.toolbar.toolbar import Toolbar


class Application(QObject):
    time_tracking_state_change = Signal(TimerStateChange)
    pause_availability_state_changed = Signal(PauseAvailability)

    def __init__(self) -> None:
        super().__init__()
        self._config = read_config_from_file()
        self._board = None
        self._pause_view = QLabel('Hi there')
        self._pause_view.setStyleSheet('border: 2px dashed red')
        self._toolbar = None
        self._new_game_dialog = None
        self._mainwindow = None
        self._set_up_game(self._config)

    @Slot()
    def on_game_start(self) -> None:
        self.time_tracking_state_change.emit(TimerStateChange.START)
        self.pause_availability_state_changed.emit(PauseAvailability.ENABLED)

    @Slot(GameOverReason)
    def on_game_over(self) -> None:
        self.time_tracking_state_change.emit(TimerStateChange.STOP)
        self.pause_availability_state_changed.emit(PauseAvailability.DISABLED)
    
    @Slot(bool)
    def on_game_paused(self, paused: bool) -> None:
        if self._mainwindow is not None:
            self._mainwindow.set_paused(paused)
            self.time_tracking_state_change.emit(TimerStateChange.STOP if paused else TimerStateChange.START)

    def _set_up_game(self, config: Config) -> None:
        write_config_to_file(config)
        self._board = Board(config)
        self._toolbar = Toolbar(self._config)
        self._mainwindow = MainWindow(self._board.view, self._pause_view, self._toolbar.view)
        # Connections
        self._board.game_started.connect(self.on_game_start)
        self._board.game_over.connect(self.on_game_over)
        self._board.flag_changed.connect(self._toolbar.on_flag_count_change)
        self.time_tracking_state_change.connect(self._toolbar.on_time_tracking_state_change)
        self._toolbar.game_paused.connect(self.on_game_paused)
        self.pause_availability_state_changed.connect(self._toolbar.on_pause_availability_change)
