from collections.abc import Iterator
from random import sample
from typing import override

from PySide6.QtCore import QSize, Signal, Slot
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QFrame, QGridLayout, QSizePolicy

from qmines.board.tile import Tile
from qmines.state.state_manager import State, StateManager
from qmines.utilities import convert_coordinates_to_index, convert_index_to_coordinates, proximity_iterator


class Board(QFrame):

    board_reappeared = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._state_manager = StateManager()
        self._config = self._state_manager.config
        self._height_to_width_ratio = self.n_rows / self.n_cols
        self._tiles = [Tile(convert_index_to_coordinates(idx, self.n_rows, self.n_cols)) for idx in range(0, self.board_size)]
        self._set_size_properties()
        self._set_layout_properties()
        self._set_up_connections()
    
    @property
    def n_rows(self) -> int:
        return self._config.n_rows
    @property
    def n_cols(self) -> int:
        return self._config.n_cols
    @property
    def n_mines(self) -> int:
        return self._config.n_mines
    @property
    def board_size(self) -> int:
        return self.n_rows * self.n_cols
    
    def __iter__(self) -> Iterator[Tile]:
        return iter(self._tiles)
    
    def __getitem__(self, coordinates: tuple[int, int]) -> Tile:
        idx = convert_coordinates_to_index(*coordinates, self.n_rows, self.n_cols)
        return self._tiles[idx]
    
    @Slot(int, int)
    def on_first_click(self, row: int, col: int) -> None:
        self._allocate_mines_and_proximities(row, col)
        self._state_manager.state = State.ACTIVE
    
    @Slot(int, int)
    def on_tile_revealed(self, row: int, col: int) -> None:
        if self[row, col].proximity_number == 0:
            for tile in proximity_iterator(self, row, col):
                tile.on_left_click()
    
    @Slot(int, int)
    def on_revealed_tile_clicked(self, row: int, col: int) -> None:
        clicked_tile = self[row, col]
        number_of_nearby_flags = sum(1 for t in proximity_iterator(self, row, col) if t.is_flagged and not t.is_revealed)
        if number_of_nearby_flags == clicked_tile.proximity_number:
            for tile in (t for t in proximity_iterator(self, row, col) if not t.is_revealed):
                tile.on_left_click()

    
    @Slot(State, State)
    def on_state_change(self, previous: State, current: State) -> None:
        match current:
            case State.PAUSED:
                if previous == State.ACTIVE:
                    self.hide()
            case State.ACTIVE:
                if previous == State.PAUSED:
                    self.show()
                    self.board_reappeared.emit()
    
    @override
    def resizeEvent(self, event: QResizeEvent):
        size = event.size()
        height = size.height()
        width = size.width()
        if height <= width * self._height_to_width_ratio:
            self.resize(QSize(round(height / self._height_to_width_ratio), height))
        else:
            self.resize(QSize(width, round(width * self._height_to_width_ratio)))
    
    def _set_size_properties(self) -> None:
        size_policy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        size_policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(size_policy)
    
    def _set_layout_properties(self) -> None:
        layout = QGridLayout()
        for tile in self:
            layout.addWidget(tile, tile.coordinates[0], tile.coordinates[1])
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
    
    def _allocate_mines_and_proximities(self, row: int, col: int) -> None:
        mine_tiles = sample([t for t in self if t.coordinates != (row, col)], self.n_mines)
        for tile in mine_tiles:
            tile.is_mine = True
        for tile in (t for t in self if not t.is_mine):
            proximity_number = 0
            for t in proximity_iterator(self, *tile.coordinates):
                if t.is_mine:
                    proximity_number += 1
            tile.proximity_number = proximity_number
    
    def _set_up_connections(self) -> None:
        self._state_manager.first_click_in_game.connect(self.on_first_click)
        self._state_manager.tile_revealed.connect(self.on_tile_revealed)
        self._state_manager.revealed_tile_clicked.connect(self.on_revealed_tile_clicked)
        self._state_manager.state_change.connect(self.on_state_change)