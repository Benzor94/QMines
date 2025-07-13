from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLabel

from qmines.constants import Symbol
from qmines.state.state_manager import FlagCountChange, State, StateManager


class MineCounter(QLabel):
    def __init__(self) -> None:
        super().__init__('')
        self._state_manager = StateManager()
        self._number_of_remaining_mines = self._state_manager.config.n_mines
        self._state_manager.flag_count_change.connect(self.on_flag_count_change)
        self._state_manager.state_change.connect(self.on_state_change)
        self._update_text()

    @Slot(FlagCountChange)
    def on_flag_count_change(self, change: FlagCountChange) -> None:
        self._number_of_remaining_mines -= change.value
        self._update_text()

    @Slot(State, State)
    def on_state_change(self, _, current: State) -> None:
        if current == State.WIN:
            self._number_of_remaining_mines = 0
            self._update_text()

    def _update_text(self) -> None:
        self.setText(f'{Symbol.MINE.value}: {self._number_of_remaining_mines}')
