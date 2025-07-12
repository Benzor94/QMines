from PySide6.QtWidgets import QLabel, QStatusBar

from qmines.status_bar.mine_counter import MineCounter
from qmines.status_bar.status_text import StatusLabel
from qmines.status_bar.time_tracker import TimeLabel


class StatusBar(QStatusBar):

    def __init__(self):
        super().__init__()
        self._status_label = StatusLabel()
        self._mine_counter = MineCounter()
        self._time_label = TimeLabel()
        self.addWidget(self._status_label)
        self.addPermanentWidget(self._mine_counter)
        self.addPermanentWidget(self._time_label)
        self.setSizeGripEnabled(False)
        # TBD