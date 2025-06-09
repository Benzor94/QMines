from typing import override, Final

import PySide6.QtWidgets as QW
import PySide6.QtGui as QG
import PySide6.QtCore as QC

from qmines.board.board import Board
from qmines.board.tile import Tile
from qmines.control_panel.control_panel import ControlPanel
from qmines.control_panel.mine_counter import MineCounter
from qmines.control_panel.new_game_button import NewGameButton
from qmines.control_panel.pause_button import PauseButton
from qmines.control_panel.time_tracker import TimeTracker
from qmines.game_parameters.game_parameters import GameParameters
from qmines.game_parameters.settings_reader import read_settings
from qmines.constants import Symbol
from qmines.utilities import set_font_size_based_on_height


class MainWindow(QW.QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self._parameters: GameParameters
        self._board: Board
        self._control_panel: ControlPanel
        self._frame: QW.QFrame
        self._layout: QW.QVBoxLayout
        self.set_up()
    
    def set_up(self, parameters: GameParameters | None = None) -> None:
        if parameters is None:
            parameters = read_settings()
        self._parameters = parameters
        #self._set_fixed_size()
        self._set_toolbar()
        self._frame = QW.QFrame()
        #new_game_btn = NewGameButton()
        #pause_btn = PauseButton()
        #mine_counter = MineCounter()
        #time_tracker = TimeTracker()
        #self._control_panel = ControlPanel(new_game_btn, pause_btn, mine_counter, time_tracker)
        self._board = self._board_factory()

        self._layout = QW.QVBoxLayout()
        #self._layout.addWidget(self._control_panel)
        self._layout.addWidget(self._board)
        self._frame.setLayout(self._layout)

        self.setSizePolicy(QW.QSizePolicy.Policy.Minimum, QW.QSizePolicy.Policy.Minimum)
        self.setCentralWidget(self._frame)
        self.show()
    
    def _board_factory(self) -> Board:
        """Temporary"""
        assert self._parameters is not None
        tiles = [Tile((idx // self._parameters.n_cols, idx % self._parameters.n_cols)) for idx in range(self._parameters.number_of_elements)]
        return Board(parameters=self._parameters, tiles=tiles)

    def _set_fixed_size(self) -> None:
        if (layout := self.layout()) is not None:
            layout.setSizeConstraint(QW.QLayout.SizeConstraint.SetFixedSize)

    def _set_toolbar(self) -> None:
        control_panel = QW.QToolBar('Control panel')
        self.addToolBar(control_panel)
        control_panel.toggleViewAction().setEnabled(False)
        control_panel.setMovable(False)

        new_game_action = QG.QAction('New', self)
        new_game_action.setStatusTip('Starts a new game')
        pause_action = QG.QAction(Symbol.PAUSE.value, self)
        pause_action.setStatusTip('Pause/unpause the game')
        set_font_size_based_on_height(pause_action, 30)
        mine_counter = QG.QAction(f'{Symbol.MINE.value}: 3 / 10', self)
        time_tracker = QG.QAction(f'{Symbol.TIMER.value}: 120 / {Symbol.INFINITY.value}', self)

        control_panel.addAction(new_game_action)
        control_panel.addAction(pause_action)
        control_panel.addSeparator()
        control_panel.addAction(mine_counter)
        control_panel.addAction(time_tracker)
    