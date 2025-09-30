from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import QSizePolicy, QToolBar, QWidget

from qmines.toolbar.counters import MineCounter, TimeTracker


class ToolbarView(QToolBar):

    def __init__(self, new_game_action: QAction, pause_action: QAction, mine_counter: MineCounter, time_tracker: TimeTracker) -> None:
        super().__init__()
        self._new_game_action = new_game_action
        self._pause_action = pause_action
        self._mine_counter = mine_counter
        self._time_tracker = time_tracker
        self._set_toolbar_properties()
        self._add_buttons()
    
    @property
    def time_tracker(self) -> TimeTracker:
        return self._time_tracker
    
    def _set_toolbar_properties(self) -> None:
        self.toggleViewAction().setEnabled(False)
        self.setMovable(False)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setIconSize(QSize(16, 16))
        self.setFixedHeight(32)
    
    def _add_buttons(self) -> None:
        self.addAction(self._new_game_action)
        self.addSeparator()
        self.addAction(self._pause_action)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.addWidget(spacer)
        self.addWidget(self._mine_counter)
        self.addSeparator()
        self.addWidget(self._time_tracker)