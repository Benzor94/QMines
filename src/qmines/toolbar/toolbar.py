from enum import Enum

from PySide6.QtCore import QObject, QTimer, Slot

from qmines.config import Config
from qmines.toolbar.actions import NewGameAction, PauseAction
from qmines.toolbar.counters import MineCounter, TimeTracker
from qmines.toolbar.toolbar_view import ToolbarView


class TimerStateChange(Enum):
    START = 0
    STOP = 1


class Toolbar(QObject):

    def __init__(self, config: Config) -> None:
        super().__init__()
        self._timer = self._create_timer()
        self._view = ToolbarView(NewGameAction(), PauseAction(), MineCounter(config.number_of_mines), TimeTracker())
        self._seconds_elapsed = 0

    @property
    def view(self) -> ToolbarView:
        return self._view
    
    @Slot(TimerStateChange)
    def on_time_tracking_state_change(self, state_change: TimerStateChange) -> None:
        match state_change:
            case TimerStateChange.START:
                self._timer.start()
            case TimerStateChange.STOP:
                self._timer.stop()

    @Slot()
    def on_timer_period(self) -> None:
        self._seconds_elapsed += 1
        self.view.time_tracker.update_counter(self._seconds_elapsed)
    
    def _create_timer(self) -> QTimer:
        timer = QTimer()
        timer.setInterval(1000)
        timer.timeout.connect(self.on_timer_period)
        return timer
