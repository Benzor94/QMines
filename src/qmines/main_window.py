from enum import Enum
from random import sample

import PySide6.QtWidgets as QW
from PySide6.QtCore import Slot, Signal

from qmines.board.board import Board
from qmines.board.tile import Tile
from qmines.control_panel.control_panel import ControlPanel
from qmines.game_parameters.game_parameters import GameParameters
from qmines.game_parameters.settings_reader import write_settings
from qmines.status_bar.status_bar import StatusBar
from qmines.utilities.index_tools import convert_index_to_coordinates, proximity_iterator
from qmines.state_processor import StateProcessor, State

class GameOver(Enum):
    WIN = 0
    MINE_EXPLODED = 1
    TIME_RAN_OUT = 2

class MainWindow(QW.QMainWindow):

    game_over = Signal(GameOver)
    game_start = Signal(int, int)

    def __init__(self, parameters: GameParameters) -> None:
        super().__init__()
        self._signal_node = StateProcessor()
        self._parameters = parameters
        self._board: Board
        self._control_panel: ControlPanel
        self._status_bar: StatusBar
        self._frame: QW.QFrame
        self._frame_layout: QW.QVBoxLayout
        self._unrevealed_tiles: int
        self.set_up(parameters)
        # To set non-resizable
        """
        if (l := self.layout()) is not None:
            l.setSizeConstraint(QW.QLayout.SizeConstraint.SetFixedSize)
        """
    
    def set_up(self, parameters: GameParameters) -> None:
        self._signal_node.state = State.INACTIVE
        self._remove_toolbars()
        self._parameters = parameters
        self._unrevealed_tiles = self._parameters.number_of_elements
        self._set_toolbar()
        self._set_statusbar()
        self._frame = QW.QFrame()
        self._set_board()

        self._frame_layout = QW.QVBoxLayout()
        self._frame_layout.addWidget(self._board)
        self._frame.setLayout(self._frame_layout)

        self.setSizePolicy(QW.QSizePolicy.Policy.Minimum, QW.QSizePolicy.Policy.Minimum)
        self.setCentralWidget(self._frame)
        self.show()

    @Slot(GameParameters)
    def on_new_game(self, parameters: GameParameters) -> None:
        self.set_up(parameters)
        self.adjustSize()
        write_settings(parameters)

    @Slot(bool)
    def on_pause(self, paused: bool) -> None:
        if paused:
            self._board.hide()
            self._signal_node.state = State.PAUSED
            self._status_bar.status_text.setText(self._signal_node.state.value)
        else:
            self._board.show()
            self._signal_node.state = State.ACTIVE
            self._status_bar.status_text.setText(self._signal_node.state.value)

    @Slot(int, int)
    def on_first_click(self, i: int, j: int) -> None:
        self._set_up_mines(i, j)
        self._signal_node.state = State.ACTIVE
        self._status_bar.status_text.setText(self._signal_node.state.value)
        self.game_start.emit(i, j)

    @Slot(int, int, bool)
    def on_tile_revealed(self, i: int, j: int, is_mine: bool) -> None:
        print(f'Tile ({i}, {j}) has been revealed. Is mine: {is_mine}')
        if self._board[i, j].proximity_number == 0:
            for neighbour in proximity_iterator(self._board, i, j):
                neighbour.left_clicked.emit()

    @Slot(int, int)
    def on_revealed_tile_clicked(self, i: int, j: int) -> None:
        ...

    def _set_board(self) -> None:
        tiles = [self._tile_factory(idx) for idx in range(self._parameters.number_of_elements)]
        self._board = Board(parameters=self._parameters, tiles=tiles)

    def _set_toolbar(self) -> None:
        self._control_panel = ControlPanel(self._parameters)
        self.addToolBar(self._control_panel)
        self._control_panel.new_game_dialog.start_new_game.connect(self.on_new_game)
        self._control_panel.pause_state_change.connect(self.on_pause)
        self.game_over.connect(self._control_panel.on_game_over)
        self.game_start.connect(self._control_panel.on_game_start)

    def _remove_toolbars(self) -> None:
        for tb in self.findChildren(QW.QToolBar):
            self.removeToolBar(tb)
    
    def _set_statusbar(self) -> None:
        self._status_bar = StatusBar(self._parameters)
        self.setStatusBar(self._status_bar)

    def _tile_factory(self, idx: int) -> Tile:
        tile = Tile(convert_index_to_coordinates(idx, self._parameters.n_rows, self._parameters.n_cols))
        tile.first_click_in_game.connect(self.on_first_click)
        tile.tile_revealed.connect(self.on_tile_revealed)
        tile.revealed_tile_clicked.connect(self.on_revealed_tile_clicked)
        self.game_start.connect(tile.on_game_start)
        return tile

    def _set_up_mines(self, clicked_row: int, clicked_column: int) -> None:
        mine_tiles = sample([t for t in self._board if t.coordinates != (clicked_row, clicked_column)], self._parameters.n_mines)
        for tile in mine_tiles:
            tile.is_mine = True
        for tile in (t for t in self._board if not t.is_mine):
            proximity_number = 0
            for t in proximity_iterator(self._board, *tile.coordinates):
                if t.is_mine:
                    proximity_number += 1
            tile.proximity_number = proximity_number

    