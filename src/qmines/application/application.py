from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QApplication, QDialog

from qmines.application.about_message import AboutMessage
from qmines.application.game_over_message import GameOverMessage
from qmines.application.mainwindow import MainWindow
from qmines.application.pause_view import PauseView
from qmines.application.start_over_message import StartOverMessage
from qmines.board.board import Board
from qmines.common import GameOverReason
from qmines.config import Config, read_config_from_file, write_config_to_file
from qmines.controls.control_manager import ControlManager
from qmines.new_game_selector.new_game_dialog import NewGameDialog


class Application(QObject):
    time_tracking_state_change = Signal(ControlManager.TimerStateChange)
    pause_availability_state_changed = Signal(ControlManager.PauseAvailability)
    game_over = Signal(GameOverReason)  # Currently only affects the mine counter

    def __init__(self) -> None:
        super().__init__()
        self._config = read_config_from_file()
        self._game_started = False
        self._game_over = False
        self._paused = False
        self._board = None
        self._pause_view = None
        self._control_manager = None
        self._new_game_dialog = None
        self._mainwindow = None
        self._set_up_game(self._config)

    @Slot()
    def on_game_start(self) -> None:
        self._game_started = True
        self.time_tracking_state_change.emit(ControlManager.TimerStateChange.START)
        self.pause_availability_state_changed.emit(ControlManager.PauseAvailability.ENABLED)

    @Slot(GameOverReason)
    def on_game_over(self, reason: GameOverReason) -> None:
        self.time_tracking_state_change.emit(ControlManager.TimerStateChange.STOP)
        self.pause_availability_state_changed.emit(ControlManager.PauseAvailability.DISABLED)
        self.game_over.emit(reason)
        self._game_over = True
        result = GameOverMessage(reason).exec()
        if result == GameOverMessage.StandardButton.Ok:
            self.on_new_game()

    @Slot(bool)
    def on_game_paused(self, paused: bool) -> None:
        if self._mainwindow is not None and not self._game_over and self._game_started:
            self._paused = paused
            self._mainwindow.set_paused(paused)
            self.time_tracking_state_change.emit(ControlManager.TimerStateChange.STOP if paused else ControlManager.TimerStateChange.START)

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

    @Slot()
    def on_game_reset(self) -> None:
        if self._game_over or not self._game_started:
            self._set_up_game(self._config)
        else:
            is_already_paused = self._paused
            if not is_already_paused:
                self.on_game_paused(True)
            result = StartOverMessage().exec()
            if not is_already_paused:
                self.on_game_paused(False)
            if result == StartOverMessage.StandardButton.Ok:
                self._set_up_game(self._config)
    
    @Slot()
    def on_game_quit(self) -> None:
        app = QApplication.instance()
        if app is not None:
            app.quit()
    
    @Slot()
    def on_about_message_invoked(self) -> None:
        is_already_paused = self._paused
        if not is_already_paused:
            self.on_game_paused(True)
        AboutMessage().exec()
        if not is_already_paused:
            self.on_game_paused(False)

    def _set_up_game(self, config: Config) -> None:
        write_config_to_file(config)
        self._config = config
        self._game_over = False
        self._board = Board(config)
        self._control_manager = ControlManager(self._config)
        self._pause_view = PauseView()
        self._mainwindow = MainWindow(self._board.view, self._pause_view, self._control_manager.toolbar, self._control_manager.menubar)
        # Connections
        # Board
        self._board.game_started.connect(self.on_game_start)
        self._board.game_over.connect(self.on_game_over)
        self._board.flag_changed.connect(self._control_manager.on_flag_count_change)
        # Control manager
        self.time_tracking_state_change.connect(self._control_manager.on_time_tracking_state_change)
        self._control_manager.game_paused.connect(self.on_game_paused)
        self.pause_availability_state_changed.connect(self._control_manager.on_pause_availability_change)
        self._control_manager.new_game.connect(self.on_new_game)
        self.game_over.connect(self._control_manager.on_game_over)
        self._control_manager.start_over_game.connect(self.on_game_reset)
        self._control_manager.game_quit.connect(self.on_game_quit)
        self._control_manager.about_dialog_invoked.connect(self.on_about_message_invoked)
