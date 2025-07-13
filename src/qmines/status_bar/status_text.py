from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLabel

from qmines.state.state_manager import State, StateManager, state_text_map


class StatusLabel(QLabel):
    def __init__(self) -> None:
        super().__init__(state_text_map[State.INACTIVE])
        self._state_manager = StateManager()
        self._state_manager.state_change.connect(self.on_state_change)

    @Slot(State, State)
    def on_state_change(self, _: State, current: State) -> None:
        self.setText(state_text_map[current])
