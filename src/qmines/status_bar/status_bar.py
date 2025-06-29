from PySide6.QtWidgets import QStatusBar, QLabel
from PySide6.QtCore import Slot

from qmines.game_parameters.game_parameters import GameParameters
from qmines.state_processor import FlagCountChange, StateProcessor
from qmines.utilities.constants import Symbol

class StatusBar(QStatusBar):
    def __init__(self, parameters: GameParameters) -> None:
        super().__init__()
        self._mines_found = 0
        self._parameters = parameters
        self._state_processor = StateProcessor()
        self._status_text = QLabel(self._state_processor.state.value)
        self._mine_counter = QLabel('')
        self._update_mine_counter_text()
        self._time_tracker_text = QLabel(f'{Symbol.TIMER.value}: {0} / {(Symbol.INFINITY.value if self._parameters.time_limit_in_seconds == 0
                                                        else self._parameters.time_limit_in_seconds)}')  # Placeholder
        self.addWidget(self._status_text)
        self.addPermanentWidget(self._mine_counter)
        self.addPermanentWidget(self._time_tracker_text)
        self.setSizeGripEnabled(False)
    
    @property
    def status_text(self) -> QLabel:  # Temporary
        return self._status_text
    
    @Slot(FlagCountChange)
    def on_flag_count_change(self, change: FlagCountChange) -> None:
        self._mines_found += change.value
        self._update_mine_counter_text()
    
    def _update_mine_counter_text(self) -> None:
        self._mine_counter.setText(f'{Symbol.FLAG.value}: {self._mines_found} / {self._parameters.n_mines}')