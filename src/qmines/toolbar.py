from typing import Final

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar

from qmines.constants import Symbol
from qmines.state.state_manager import State, StateManager
from qmines.utilities import set_font_size_based_on_height


class Toolbar(QToolBar):

    BAR_HEIGHT: Final[int] = 30

    def __init__(self) -> None:
        super().__init__('Control panel')        
        self._state_manager = StateManager()

        self._new_game_action = self._create_new_game_action()
        self._pause_action = self._create_pause_action()

        self._add_toolbar_buttons()
        self._set_toolbar_properties()
    
    @Slot(State, State)
    def on_state_change(self, previous: State, current: State) -> None:
        match current:
            case State.ACTIVE:
                if previous == State.INACTIVE:
                    self._pause_action.setEnabled(True)
            case State.WIN | State.LOSS_MINE_HIT | State.LOSS_TIMEOUT:
                self._pause_action.setChecked(False)
                self._pause_action.setEnabled(False)
    
    @Slot(bool)
    def on_pause_action(self, paused: bool) -> None:
        if paused:
            self._state_manager.state = State.PAUSED
        else:
            self._state_manager.state = State.ACTIVE
    
    def _create_new_game_action(self) -> QAction:
        new_game_action = QAction('New')
        new_game_action.setToolTip('Start a new game')
        # Connections
        return new_game_action
    
    def _create_pause_action(self) -> QAction:
        pause_action = QAction(Symbol.PAUSE.value)
        pause_action.setToolTip('Pause/resume the game')
        pause_action.setCheckable(True)
        set_font_size_based_on_height(pause_action, self.BAR_HEIGHT)
        pause_action.setEnabled(False)
        pause_action.toggled.connect(self.on_pause_action)
        return pause_action
    
    def _add_toolbar_buttons(self) -> None:
        self.addAction(self._new_game_action)
        self.addSeparator()
        self.addAction(self._pause_action)
    
    def _set_toolbar_properties(self) -> None:
        self.toggleViewAction().setEnabled(False)
        self.setMovable(False)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)

# TODO: Probably Pause and New Game actions should be separate classes and thus toolbar should be moved to a separate package