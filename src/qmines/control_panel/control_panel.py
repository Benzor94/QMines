import PySide6.QtWidgets as QW
import PySide6.QtGui as QG
import PySide6.QtCore as QC

from qmines.constants import Symbol
from qmines.utilities import set_font_size_based_on_height


class ControlPanel(QW.QToolBar):
    def __init__(self) -> None:
        super().__init__('Control panel')
        self._new_game_action = self._get_new_game_action()
        self._pause_action = self._get_pause_action()
        self._mine_counter = self._get_mine_counter()
        self._time_tracker = self._get_time_tracker()
        self.toggleViewAction().setEnabled(False)
        self.setMovable(False)

        self.addAction(self._new_game_action)
        self.addSeparator()
        self.addAction(self._pause_action)
        self.addWidget(self._get_spacer())
        self.addAction(self._mine_counter)
        self.addSeparator()
        self.addAction(self._time_tracker)
        self.setToolButtonStyle(QC.Qt.ToolButtonStyle.ToolButtonTextOnly)

    @staticmethod
    def _get_new_game_action() -> QG.QAction:
        new_game_action = QG.QAction('New')
        new_game_action.setToolTip('Start a new game')
        return new_game_action

    @staticmethod
    def _get_pause_action() -> QG.QAction:
        pause_action = QG.QAction(Symbol.PAUSE.value)
        pause_action.setToolTip('Pause/resume the game')
        set_font_size_based_on_height(pause_action, 30)
        return pause_action

    @staticmethod
    def _get_spacer() -> QW.QWidget:
        spacer = QW.QWidget()
        spacer.setSizePolicy(QW.QSizePolicy.Policy.Expanding, QW.QSizePolicy.Policy.Preferred)
        return spacer

    @staticmethod
    def _get_mine_counter() -> QG.QAction:
        mine_counter = QG.QAction(f'{Symbol.MINE.value}: 3 / 10')
        mine_counter.setToolTip('Flagged mines / total')
        return mine_counter

    @staticmethod
    def _get_time_tracker() -> QG.QAction:
        time_tracker = QG.QAction(f'{Symbol.TIMER.value}: 120 / {Symbol.INFINITY.value}')
        time_tracker.setToolTip('Seconds spent in current game / time limit')
        return time_tracker