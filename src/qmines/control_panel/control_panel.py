import PySide6.QtWidgets as QW

from qmines.control_panel.mine_counter import MineCounter
from qmines.control_panel.new_game_button import NewGameButton
from qmines.control_panel.pause_button import PauseButton
from qmines.control_panel.time_tracker import TimeTracker

class ControlPanel(QW.QFrame):
    def __init__(self, new_game_btn: NewGameButton, pause_btn: PauseButton, mine_counter: MineCounter, time_tracker: TimeTracker) -> None:
        super().__init__()
        self._new_game_button = new_game_btn
        self._pause_button = pause_btn
        self._mine_counter = mine_counter
        self._time_tracker = time_tracker

        self._layout = QW.QHBoxLayout()
        self._layout.addWidget(self._new_game_button)
        self._layout.addSpacerItem(QW.QSpacerItem(0, 0, QW.QSizePolicy.Policy.MinimumExpanding))
        self._layout.addWidget(self._pause_button)
        self._layout.addSpacerItem(QW.QSpacerItem(0, 0, QW.QSizePolicy.Policy.MinimumExpanding))
        self._layout.addWidget(self._mine_counter)
        self._layout.addSpacerItem(QW.QSpacerItem(0, 0, QW.QSizePolicy.Policy.MinimumExpanding))
        self._layout.addWidget(self._time_tracker)
        self.setLayout(self._layout)