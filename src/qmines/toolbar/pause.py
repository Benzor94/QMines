from typing import Final

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction

from qmines.constants import Symbol
from qmines.state.state_manager import State, StateManager
from qmines.utilities import set_font_size_based_on_height


class PauseAction(QAction):

    BAR_HEIGHT: Final[int] = 30

    def __init__(self) -> None:
        super().__init__(Symbol.PAUSE.value)
        self._state_manager = StateManager()
        self.setToolTip('Pause/resume the game')
        self.setCheckable(True)
        set_font_size_based_on_height(self, self.BAR_HEIGHT)
        self.setEnabled(False)
        self.toggled.connect(self.on_pause_action)
    
    @Slot(bool)
    def on_pause_action(self, paused: bool) -> None:
        if paused:
            self._state_manager.state = State.PAUSED
        else:
            self._state_manager.state = State.ACTIVE
    
    @Slot(State, State)
    def on_state_change(self, previous: State, current: State) -> None:
        match current:
            case State.ACTIVE:
                if previous == State.INACTIVE:
                    self.setEnabled(True)
            case State.WIN | State.LOSS_MINE_HIT | State.LOSS_TIMEOUT:
                self.setChecked(False)
                self.setEnabled(False)