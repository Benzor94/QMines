from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar

from qmines.dialog.new_game.new_game_dialog import NewGameDialog
from qmines.state.state_manager import State, StateManager
from qmines.toolbar.pause import PauseAction


class Toolbar(QToolBar):
    def __init__(self) -> None:
        super().__init__('Control panel')
        self._state_manager = StateManager()
        self._paused_before_new_game_button_press = False

        self._new_game_dialog = self._create_new_game_dialog()

        self._new_game_action = self._create_new_game_action()
        self._pause_action = PauseAction()

        self._add_toolbar_buttons()
        self._set_toolbar_properties()

    @Slot()
    def on_new_game_button_press(self) -> None:
        if self._state_manager.state == State.PAUSED:
            self._paused_before_new_game_button_press = True
        else:
            self._pause_action.setChecked(True)
        self._new_game_dialog.exec()

    @Slot()
    def on_new_game_dialog_rejected(self) -> None:
        if self._paused_before_new_game_button_press:
            self._paused_before_new_game_button_press = False
            return
        self._pause_action.setChecked(False)

    def _create_new_game_dialog(self) -> NewGameDialog:
        dialog = NewGameDialog(self)
        dialog.rejected.connect(self.on_new_game_dialog_rejected)
        return dialog

    def _create_new_game_action(self) -> QAction:
        new_game_action = QAction('New')
        new_game_action.setToolTip('Start a new game')
        new_game_action.triggered.connect(self.on_new_game_button_press)
        return new_game_action

    def _add_toolbar_buttons(self) -> None:
        self.addAction(self._new_game_action)
        self.addSeparator()
        self.addAction(self._pause_action)

    def _set_toolbar_properties(self) -> None:
        self.toggleViewAction().setEnabled(False)
        self.setMovable(False)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
