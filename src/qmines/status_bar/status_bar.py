from PySide6.QtWidgets import QStatusBar, QLabel
from PySide6.QtCore import Slot, QTimer

from qmines.state_processor import FlagCountChange, State, StateProcessor
from qmines.utilities.constants import Symbol

class StatusBar(QStatusBar):
    def __init__(self) -> None:
        super().__init__()
        self._mines_found = 0
        self._seconds_elapsed = 0
        self._state_processor = StateProcessor()
        self._parameters = self._state_processor.parameters
        self._status_label = QLabel(self._state_processor.state.value)
        self._mine_counter = QLabel('')
        self._update_mine_counter_text()
        self._time_limit_text = self._get_time_limit_text()
        self._time_tracker_label = QLabel(self._get_time_tracker_text())
        self._time_tracker = self._set_up_time_tracker()
        self.addWidget(self._status_label)
        self.addPermanentWidget(self._mine_counter)
        self.addPermanentWidget(self._time_tracker_label)
        self.setSizeGripEnabled(False)
        self._state_processor.flag_change.connect(self.on_flag_count_change)
        self._state_processor.state_change.connect(self.on_state_change)
    
    @Slot(FlagCountChange)
    def on_flag_count_change(self, change: FlagCountChange) -> None:
        self._mines_found += change.value
        self._update_mine_counter_text()
    
    @Slot(State, State)
    def on_state_change(self, _: State, current: State) -> None:
        self._status_label.setText(current.value)
        match current:
            case State.ACTIVE:
                self._time_tracker.start()
            case _:
                self._time_tracker.stop()
    
    @Slot()
    def on_timer_period(self) -> None:
        self._seconds_elapsed += 1
        self._time_tracker_label.setText(self._get_time_tracker_text())
        if (lim := self._parameters.time_limit_in_seconds) and self._seconds_elapsed >= lim:
            self._state_processor.state = State.LOSS_TIMEOUT
    
    def _update_mine_counter_text(self) -> None:
        self._mine_counter.setText(f'{Symbol.FLAG.value}: {self._mines_found} / {self._parameters.n_mines}')
    
    def _set_up_time_tracker(self) -> QTimer:
        timer = QTimer()
        timer.setInterval(1000)
        timer.timeout.connect(self.on_timer_period)
        return timer
    
    def _get_time_limit_text(self) -> str:
        time_limit = self._parameters.time_limit_in_seconds
        time_limit_text = f'{time_limit} s' if time_limit else Symbol.INFINITY.value
        return time_limit_text
    
    def _get_time_tracker_text(self) -> str:
        current_time = self._seconds_elapsed
        current_time_text = f'{current_time} s'
        time_tracker_text = f'{Symbol.TIMER.value}: {current_time_text} / {self._time_limit_text}'
        return time_tracker_text
