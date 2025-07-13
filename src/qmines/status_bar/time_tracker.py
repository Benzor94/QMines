from PySide6.QtCore import QTimer, Slot
from PySide6.QtWidgets import QLabel

from qmines.constants import Symbol
from qmines.state.state_manager import State, StateManager


class TimeLabel(QLabel):
    def __init__(self) -> None:
        super().__init__('')
        self._state_manager = StateManager()
        self._timer = self._create_timer()
        self._seconds_elapsed = 0
        self._time_limit = self._state_manager.config.time_limit
        self._state_manager.state_change.connect(self.on_state_change)
        self._update_text()

    @Slot(State, State)
    def on_state_change(self, _, current: State) -> None:
        if current == State.ACTIVE:
            self._timer.start()
        else:
            self._timer.stop()

    @Slot()
    def on_timer_period_elapsed(self) -> None:
        self._seconds_elapsed += 1
        self._update_text()
        if self._time_limit and self._seconds_elapsed >= self._time_limit:
            self._state_manager.state = State.LOSS_TIMEOUT

    def _create_timer(self) -> QTimer:
        timer = QTimer()
        timer.setInterval(1000)
        timer.timeout.connect(self.on_timer_period_elapsed)
        return timer

    def _update_text(self) -> None:
        display_time = self._time_limit - self._seconds_elapsed if self._time_limit else self._seconds_elapsed
        self.setText(f'{Symbol.TIMER.value}: {display_time} s')
