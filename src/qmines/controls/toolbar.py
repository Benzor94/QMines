from typing import Final

from PySide6.QtCore import QSize
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QSizePolicy, QToolBar, QWidget

from qmines.controls.actions import NewGameAction, PauseAction, ResetGameAction
from qmines.controls.counters import MineCounter, TimeTracker


class Toolbar(QToolBar):
    HEIGHT: Final[int] = 40
    ICON_SIZE: Final[int] = 20

    def __init__(self, new_game_action: NewGameAction, reset_action: ResetGameAction, pause_action: PauseAction, mine_counter: MineCounter, time_tracker: TimeTracker) -> None:
        super().__init__()
        self._new_game_action = new_game_action
        self._reset_action = reset_action
        self._pause_action = pause_action
        self._mine_counter = mine_counter
        self._time_tracker = time_tracker
        self._set_toolbar_properties()
        self._add_buttons()

    def _set_toolbar_properties(self) -> None:
        self.toggleViewAction().setEnabled(False)
        self.setMovable(False)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setIconSize(QSize(self.ICON_SIZE, self.ICON_SIZE))
        self.setFixedHeight(self.HEIGHT)

    def _add_buttons(self) -> None:
        self.addAction(self._new_game_action)
        self.addSeparator()
        self.addAction(self._reset_action)
        self.addSeparator()
        self.addAction(self._pause_action)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.addWidget(spacer)
        self.addWidget(self._mine_counter)
        self.addSeparator()
        self.addWidget(self._time_tracker)
