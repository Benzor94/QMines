from typing import override, Final

import PySide6.QtWidgets as QW
import PySide6.QtGui as QG
import PySide6.QtCore as QC

from qmines.control_panel.mine_counter import MineCounter
from qmines.control_panel.new_game_button import NewGameButton
from qmines.control_panel.pause_button import PauseButton
from qmines.control_panel.time_tracker import TimeTracker
from qmines.constants import CONTROL_PANEL_MIN_HEIGHT, CONTROL_PANEL_MAX_HEIGHT

class ControlPanel(QW.QFrame):

    def __init__(self, new_game_btn: NewGameButton, pause_btn: PauseButton, mine_counter: MineCounter, time_tracker: TimeTracker) -> None:
        super().__init__()
        self._new_game_button = new_game_btn
        self._pause_button = pause_btn
        self._mine_counter = mine_counter
        self._time_tracker = time_tracker

        self._layout = QW.QHBoxLayout()
        self._set_size_properties()
        self._set_layout_properties()
    
    def _set_size_properties(self) -> None:
        self.setSizePolicy(QW.QSizePolicy(QW.QSizePolicy.Policy.Minimum, QW.QSizePolicy.Policy.Minimum))
        self.setMaximumHeight(CONTROL_PANEL_MAX_HEIGHT)
        self.setMinimumHeight(CONTROL_PANEL_MIN_HEIGHT)
    
    def _set_layout_properties(self) -> None:
        self._layout.addWidget(self._new_game_button)
        #self._layout.addSpacerItem(QW.QSpacerItem(0, 0, QW.QSizePolicy.Policy.MinimumExpanding))
        self._layout.addWidget(self._pause_button)
        #self._layout.addSpacerItem(QW.QSpacerItem(0, 0, QW.QSizePolicy.Policy.MinimumExpanding))
        self._layout.addWidget(self._mine_counter)
        #self._layout.addSpacerItem(QW.QSpacerItem(0, 0, QW.QSizePolicy.Policy.MinimumExpanding))
        self._layout.addWidget(self._time_tracker)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)