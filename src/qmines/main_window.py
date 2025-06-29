from random import sample
from threading import Lock

import PySide6.QtWidgets as QW
from PySide6.QtCore import Slot, QSize

from qmines.board.board import Board
from qmines.board.tile import Tile
from qmines.control_panel.control_panel import ControlPanel
from qmines.game_parameters.settings_reader import write_settings
from qmines.status_bar.status_bar import StatusBar
from qmines.utilities.index_tools import convert_index_to_coordinates, proximity_iterator
from qmines.state_processor import StateProcessor, State


class MainWindow(QW.QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self._state_processor = StateProcessor()
        self._lock = Lock()
        self._parameters = self._state_processor.parameters
        self._board: Board
        self._control_panel: ControlPanel
        self._status_bar: StatusBar
        self._frame: QW.QFrame
        self._frame_layout: QW.QVBoxLayout
        self._unrevealed_tiles: int
        self._set_up_connections()
        self.set_up()
        # To set non-resizable
        """
        if (l := self.layout()) is not None:
            l.setSizeConstraint(QW.QLayout.SizeConstraint.SetFixedSize)
        """
    
    def set_up(self) -> None:
        self._remove_toolbars()
        self._parameters = self._state_processor.parameters
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
    
    @Slot(State, State)
    def on_state_change(self, previous: State, current: State) -> None:
        match current:
            case State.INACTIVE:
                self._on_new_game()
            case State.ACTIVE:
                if previous == State.PAUSED:
                    self._on_pause(False)
            case State.PAUSED:
                if previous == State.ACTIVE:
                    self._on_pause(True)
            case State.WIN | State.LOSS_TIMEOUT | State.LOSS_MINE_HIT:
                ...

    @Slot(int, int)
    def on_first_click(self, row: int, col: int) -> None:
        self._set_up_mines(row, col)
        self._state_processor.state = State.ACTIVE
        self._board[row, col].on_left_click()

    @Slot(int, int)
    def on_tile_revealed(self, row: int, col: int) -> None:
        tile = self._board[row, col]
        print(f'Tile ({row}, {col}) has been revealed. Is mine: {tile.is_mine}')
        if tile.is_mine:
            self._state_processor.state = State.LOSS_MINE_HIT
        else:
            with self._lock:
                self._unrevealed_tiles -= 1
            if self._unrevealed_tiles == self._parameters.n_mines:
                self._state_processor.state = State.WIN
            if self._board[row, col].proximity_number == 0:
                for neighbour in proximity_iterator(self._board, row, col):
                    neighbour.left_clicked.emit()

    @Slot(int, int)
    def on_revealed_tile_clicked(self, row: int, col: int) -> None:
        clicked_tile = self._board[row, col]
        proximity = clicked_tile.proximity_number
        number_of_nearby_flags = sum(1 for t in proximity_iterator(self._board, row, col) if not t.is_revealed and t.is_flagged)
        if proximity == number_of_nearby_flags:
            for tile in (t for t in proximity_iterator(self._board, row, col) if not t.is_revealed):
                tile.on_left_click()

    def _set_board(self) -> None:
        tiles = [self._tile_factory(idx) for idx in range(self._parameters.number_of_elements)]
        self._board = Board(tiles)

    def _set_toolbar(self) -> None:
        self._control_panel = ControlPanel()
        self.addToolBar(self._control_panel)

    def _remove_toolbars(self) -> None:
        for tb in self.findChildren(QW.QToolBar):
            self.removeToolBar(tb)
    
    def _set_statusbar(self) -> None:
        self._status_bar = StatusBar()
        self.setStatusBar(self._status_bar)

    def _tile_factory(self, idx: int) -> Tile:
        tile = Tile(convert_index_to_coordinates(idx, self._parameters.n_rows, self._parameters.n_cols))
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

    def _resize_slightly(self) -> None:
        # To get rid of some size-based artifacts.
        # Works for unpause but not when new game is started.
        size = self.size()
        height = size.height()
        width = size.width()
        self.resize(QSize(width + 1, height + 1))
        self.resize(QSize(width, height))
    
    def _on_new_game(self) -> None:
        self.set_up()
        self.adjustSize()
        write_settings(self._state_processor.parameters)
        self._resize_slightly()
    
    def _on_pause(self, paused: bool) -> None:
        if paused:
            self._board.hide()
        else:
            self._board.show()
            self._resize_slightly()
    
    def _set_up_connections(self) -> None:
        self._state_processor.state_change.connect(self.on_state_change)
        self._state_processor.first_click.connect(self.on_first_click)
        self._state_processor.tile_revealed.connect(self.on_tile_revealed)
        self._state_processor.revealed_tile_clicked.connect(self.on_revealed_tile_clicked)

    