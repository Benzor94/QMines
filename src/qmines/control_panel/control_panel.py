import PySide6.QtWidgets as QW
import PySide6.QtGui as QG
import PySide6.QtCore as QC
from PySide6.QtCore import Signal

from qmines.state_processor import State, StateProcessor
from qmines.utilities.constants import Symbol
from qmines.control_panel.new_game_dialog import NewGameDialog
from qmines.game_parameters.game_parameters import GameParameters
from qmines.utilities import set_font_size_based_on_height


class ControlPanel(QW.QToolBar):

    def __init__(self) -> None:
        super().__init__('Control panel')
        self._state_processor = StateProcessor()

        self._new_game_dialog = NewGameDialog(self)

        self._new_game_action = self._get_new_game_action()
        self._pause_action = self._get_pause_action()
        self.toggleViewAction().setEnabled(False)
        self.setMovable(False)

        self.addAction(self._new_game_action)
        self.addSeparator()
        self.addAction(self._pause_action)
        self.setToolButtonStyle(QC.Qt.ToolButtonStyle.ToolButtonTextOnly)
        self._state_processor.state_change.connect(self.on_state_change)

    @property
    def new_game_dialog(self) -> NewGameDialog:
        return self._new_game_dialog

    @QC.Slot()
    def on_new_game_action(self):
        self.new_game_dialog.exec()
    
    @QC.Slot(bool)
    def on_pause_state_change(self, paused: bool) -> None:
        if paused:
            self._state_processor.state = State.PAUSED
        else:
            self._state_processor.state = State.ACTIVE
    
    @QC.Slot(State, State)
    def on_state_change(self, previous: State, current: State) -> None:
        match current:
            case State.ACTIVE:
                if previous == State.INACTIVE:
                    self._pause_action.setEnabled(True)
            case State.WIN | State.LOSS_MINE_HIT | State.LOSS_TIMEOUT:
                self._pause_action.setChecked(False)
                self._pause_action.setEnabled(False)

    def _get_new_game_action(self) -> QG.QAction:
        new_game_action = QG.QAction('New')
        new_game_action.setToolTip('Start a new game')
        new_game_action.triggered.connect(self.on_new_game_action)
        return new_game_action

    def _get_pause_action(self) -> QG.QAction:
        pause_action = QG.QAction(Symbol.PAUSE.value)
        pause_action.setToolTip('Pause/resume the game')
        pause_action.setCheckable(True)
        set_font_size_based_on_height(pause_action, 30)
        pause_action.toggled.connect(self.on_pause_state_change)
        pause_action.setEnabled(False)
        return pause_action