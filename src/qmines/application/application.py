import sys
from collections.abc import Callable
from functools import wraps
from typing import Concatenate

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QDialog, QMessageBox

from qmines.application.about_message import AboutMessage
from qmines.application.game_over_message import GameOverMessage
from qmines.application.mainwindow import MainWindow
from qmines.application.pause_view import PauseView
from qmines.application.start_over_message import StartOverMessage
from qmines.board.board import Board
from qmines.common import GameOverReason, get_version
from qmines.config import EASY_CONFIG, Config, read_config_from_file, write_config_to_file
from qmines.controls.control_manager import ControlManager
from qmines.new_game_selector.new_game_dialog import NewGameDialog


class Application(QObject):
    time_tracking_state_change = Signal(ControlManager.TimerStateChange)
    pause_availability_state_changed = Signal(ControlManager.PauseAvailability)
    game_over = Signal(GameOverReason)  # Currently only affects the mine counter

    @staticmethod
    def dialog_pause_guard[**P](meth: Callable[Concatenate['Application', P], None]) -> Callable[Concatenate['Application', P], None]:

        @wraps(meth)
        def inner(self: 'Application', *args: P.args, **kwargs: P.kwargs) -> None:
            if self._game_over or not self._game_started:
                is_currently_paused = True
            else:
                is_currently_paused = self._paused
            if not is_currently_paused:
                self.on_game_paused(True)
            meth(self, *args, **kwargs)
            if not is_currently_paused:
                self.on_game_paused(False)
            return
        return inner

    def __init__(self) -> None:
        super().__init__()
        self._game_started = False
        self._game_over = False
        self._paused = False
        self._board = None
        self._pause_view = None
        self._control_manager = None
        self._new_game_dialog = None
        self._mainwindow = None
        self._config = self._get_initial_config()
        self._set_up_game(self._config)

    @Slot()
    def on_game_start(self) -> None:
        self._game_started = True
        self.time_tracking_state_change.emit(ControlManager.TimerStateChange.START)
        self.pause_availability_state_changed.emit(ControlManager.PauseAvailability.ENABLED)

    @Slot(GameOverReason)
    def on_game_over(self, reason: GameOverReason) -> None:
        assert self._mainwindow is not None
        self.time_tracking_state_change.emit(ControlManager.TimerStateChange.STOP)
        self.pause_availability_state_changed.emit(ControlManager.PauseAvailability.DISABLED)
        self.game_over.emit(reason)
        self._game_over = True
        result = GameOverMessage(reason, self._mainwindow).exec()
        if result == GameOverMessage.StandardButton.Ok:
            self.on_new_game()

    @Slot(bool)
    def on_game_paused(self, paused: bool) -> None:
        if self._mainwindow is not None and not self._game_over and self._game_started:
            self._paused = paused
            self._mainwindow.set_paused(paused)
            self.time_tracking_state_change.emit(ControlManager.TimerStateChange.STOP if paused else ControlManager.TimerStateChange.START)

    @Slot()
    @dialog_pause_guard
    def on_new_game(self) -> None:
        assert self._mainwindow is not None
        dialog = NewGameDialog(self._mainwindow, self._config)
        result = QDialog.DialogCode(dialog.exec())
        config = dialog.selected_config
        if result == QDialog.DialogCode.Accepted:
            self._set_up_game(config)

    @Slot()
    @dialog_pause_guard
    def on_game_reset(self) -> None:
        assert self._mainwindow is not None
        if self._game_over or not self._game_started:
            self._set_up_game(self._config)
        else:
            result = StartOverMessage(self._mainwindow).exec()
            if result == StartOverMessage.StandardButton.Ok:
                self._set_up_game(self._config)
    
    @Slot()
    def on_game_quit(self) -> None:
        sys.exit()
    
    @Slot()
    @dialog_pause_guard
    def on_about_message_invoked(self) -> None:
        #AboutMessage(self._mainwindow).exec()
        QMessageBox.about(self._mainwindow, 'About', f'QMines {get_version()}\n\nSimple minesweeper game.')

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
        # Some combination of pause and dialog can cause the timer to go off at start, this fixes it
        self.time_tracking_state_change.emit(ControlManager.TimerStateChange.STOP)
    
    def _get_initial_config(self) -> Config:
        config = read_config_from_file()
        if config is not None:
            return config
        dialog = NewGameDialog(None, EASY_CONFIG)
        result = dialog.exec()
        config = dialog.selected_config
        if result != QDialog.DialogCode.Accepted:
            sys.exit()
        return config

    

