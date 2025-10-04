from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QDialog

from qmines.application.game_over_message import GameOverMessage
from qmines.application.mainwindow import MainWindow
from qmines.application.pause_view import PauseView
from qmines.board.board import Board
from qmines.config import Config, read_config_from_file, write_config_to_file
from qmines.common import GameOverReason
from qmines.new_game_selector.new_game_dialog import NewGameDialog
from qmines.toolbar.toolbar import Toolbar


class Application(QObject):
    time_tracking_state_change = Signal(Toolbar.TimerStateChange)
    pause_availability_state_changed = Signal(Toolbar.PauseAvailability)
    game_over = Signal(GameOverReason)  # Currently only affects the mine counter

    def __init__(self) -> None:
        super().__init__()
        self._config = read_config_from_file()
        self._game_over = False
        self._paused = False
        self._board = None
        self._pause_view = None
        self._toolbar = None
        self._new_game_dialog = None
        self._mainwindow = None
        self._set_up_game(self._config)

    @Slot()
    def on_game_start(self) -> None:
        self.time_tracking_state_change.emit(Toolbar.TimerStateChange.START)
        self.pause_availability_state_changed.emit(Toolbar.PauseAvailability.ENABLED)

    @Slot(GameOverReason)
    def on_game_over(self, reason: GameOverReason) -> None:
        self.time_tracking_state_change.emit(Toolbar.TimerStateChange.STOP)
        self.pause_availability_state_changed.emit(Toolbar.PauseAvailability.DISABLED)
        self.game_over.emit(reason)
        self._game_over = True
        result = GameOverMessage(reason).exec()
        if result == GameOverMessage.StandardButton.Ok:
            self.on_new_game()

    @Slot(bool)
    def on_game_paused(self, paused: bool) -> None:
        if self._mainwindow is not None and not self._game_over:
            self._paused = paused
            self._mainwindow.set_paused(paused)
            self.time_tracking_state_change.emit(Toolbar.TimerStateChange.STOP if paused else Toolbar.TimerStateChange.START)

    @Slot()
    def on_new_game(self) -> None:
        assert self._mainwindow is not None
        is_already_paused = self._paused
        if not is_already_paused:
            self.on_game_paused(True)
        dialog = NewGameDialog(self._mainwindow, self._config)
        result = QDialog.DialogCode(dialog.exec())
        config = dialog.selected_config
        if not is_already_paused:
            self.on_game_paused(False)
        if result == QDialog.DialogCode.Accepted:
            self._set_up_game(config)

    def _set_up_game(self, config: Config) -> None:
        write_config_to_file(config)
        self._config = config
        self._game_over = False
        self._board = Board(config)
        self._toolbar = Toolbar(self._config)
        self._pause_view = PauseView()
        self._mainwindow = MainWindow(self._board.view, self._pause_view, self._toolbar.view)
        # Connections
        self._board.game_started.connect(self.on_game_start)
        self._board.game_over.connect(self.on_game_over)
        self._board.flag_changed.connect(self._toolbar.on_flag_count_change)
        self.time_tracking_state_change.connect(self._toolbar.on_time_tracking_state_change)
        self._toolbar.game_paused.connect(self.on_game_paused)
        self.pause_availability_state_changed.connect(self._toolbar.on_pause_availability_change)
        self._toolbar.new_game.connect(self.on_new_game)
        self.game_over.connect(self._toolbar.on_game_over)
