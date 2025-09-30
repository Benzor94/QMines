from threading import Lock

from PySide6.QtCore import QObject, QTimer, Signal, Slot

from qmines.config import Config
from qmines.enums import FlagCountChange, PauseAvailability, TimerStateChange
from qmines.toolbar.actions import NewGameAction, PauseAction
from qmines.toolbar.counters import MineCounter, TimeTracker
from qmines.toolbar.toolbar_view import ToolbarView


class Toolbar(QObject):

    game_paused = Signal(bool)

    def __init__(self, config: Config) -> None:
        super().__init__()
        self._timer = self._create_timer()
        self._view = ToolbarView(NewGameAction(), PauseAction(), MineCounter(config.number_of_mines), TimeTracker())
        self._lock = Lock()
        self._seconds_elapsed = 0
        self._number_of_remaining_mines = config.number_of_mines
        self.view.pause_action.toggled.connect(self.game_paused.emit)

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
    
    @Slot(FlagCountChange)
    def on_flag_count_change(self, change: FlagCountChange) -> None:
        with self._lock:
            match change:
                case FlagCountChange.ADDED:
                    self._number_of_remaining_mines -= 1
                    
                case FlagCountChange.REMOVED:
                    self._number_of_remaining_mines += 1
            self.view.mine_counter.update_counter(self._number_of_remaining_mines)
    
    @Slot(PauseAvailability)
    def on_pause_availability_change(self, availability: PauseAvailability) -> None:
        match availability:
            case PauseAvailability.ENABLED:
                self.view.pause_action.setEnabled(True)
            case PauseAvailability.DISABLED:
                self.view.pause_action.setEnabled(False)

    @Slot()
    def on_timer_period(self) -> None:
        self._seconds_elapsed += 1
        self.view.time_tracker.update_counter(self._seconds_elapsed)

    def _create_timer(self) -> QTimer:
        timer = QTimer()
        timer.setInterval(1000)
        timer.timeout.connect(self.on_timer_period)
        return timer
