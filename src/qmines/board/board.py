from collections.abc import Iterator
from random import sample
from PySide6.QtCore import QObject, Signal, Slot

from qmines.board.board_view import BoardView
from qmines.config import Config
from qmines.tile.tile import Tile


class Board(QObject):

    flag_changed = Signal(int)
    mine_triggered = Signal()

    def __init__(self, config: Config) -> None:
        self._n_rows = config.number_of_rows
        self._n_cols = config.number_of_columns
        self._n_mines = config.number_of_mines
        self._size = self._n_rows * self._n_cols
        self._initialized = False
        self._game_over = False
        self._tiles = [self._create_tile(idx) for idx in range(self._size)]
        self._view = BoardView(self._n_rows / self._n_cols, {(t.row, t.col): t.view for t in self._tiles})
    
    def __getitem__(self, coordinates: tuple[int, int]) -> Tile:
        return self._tiles[self._coordinates_to_index(*coordinates)]
    
    def __iter__(self) -> Iterator[Tile]:
        return iter(self._tiles)
    
    @Slot(int, int)
    def on_left_click(self, row: int, col: int) -> None:
        if self._game_over:
            return
        if not self._initialized:
            self._set_up_board(row, col)
            self._initialized = True
            self.on_left_click(row, col)
            return
        clicked_tile = self[row, col]
        if clicked_tile.is_flag:
            return
        if not clicked_tile.is_revealed:
            clicked_tile.reveal()
            if clicked_tile.proximity_number == 0:
                self._cascade_reveal(row, col)
            return
        if clicked_tile.is_revealed and clicked_tile.proximity_number != 0 and not clicked_tile.is_mine:
            self._cascade_reveal(row, col)
    
    @Slot(int, int)
    def on_right_click(self, row: int, col: int) -> None:
        if self._game_over or not self._initialized:
            return
        tile = self[row, col]
        if tile.is_revealed:
            return
        if tile.is_flag:
            tile.set_flag(False)
            self.flag_changed.emit(-1)
        else:
            tile.set_flag(True)
            self.flag_changed.emit(1)
    
    def _create_tile(self, idx: int) -> Tile:
        tile = Tile(*self._index_to_coordinates(idx))
        tile.left_clicked.connect(self.on_left_click)
        tile.right_clicked.connect(self.on_right_click)
        return tile
    
    def _reveal_tile(self, tile: Tile) -> None:
        if tile.is_mine:
            tile.exploded = True
            self.mine_triggered.emit()
            self._game_over = True
            self._reveal_all_tiles()
        else:
            tile.reveal()
    
    def _reveal_all_tiles(self) -> None:
        for tile in self:
            tile.reveal()
    
    def _cascade_reveal(self, row: int, col: int) -> None:
        for neighbour in self._proximity_iterator(row, col):
            self.on_left_click(neighbour.row, neighbour.col)
    
    def _set_up_board(self, first_clicked_row: int, first_clicked_column: int) -> None:
        non_adjacent_tiles = list(self._proximity_iterator(first_clicked_row, first_clicked_column, on_complement=True))
        mines = sample(non_adjacent_tiles, self._n_mines)
        for tile in mines:
            tile.is_mine = True
        for tile in self:
            tile.proximity_number = sum(1 for n in self._proximity_iterator(tile.row, tile.col) if n.is_mine)
    
    def _coordinates_to_index(self, row: int, col: int) -> int:
        self._coordinates_on_board_check(row, col)
        return row * self._n_cols + col
    
    def _index_to_coordinates(self, idx: int) -> tuple[int, int]:
        self._index_on_board_check(idx)
        return idx // self._n_cols, idx % self._n_cols
    
    def _index_on_board_check(self, idx: int) -> None:
        if 0 <= idx < self._size:
            return
        raise IndexError(f'Index {idx} is not on the board, must be between 0 and {self._size - 1}.')
    
    def _coordinates_on_board_check(self, row: int, col: int) -> None:
        if self._is_on_board(row, col):
            return
        raise IndexError(f'Coordinates ({row}, {col}) are not on the board, which is size {self._n_rows} x {self._n_cols}.')
    
    def _is_on_board(self, row: int, col: int) -> bool:
        return 0 <= row < self._n_rows and 0 <= col < self._n_cols
    
    def _proximity_iterator(self, row: int, col: int, *, on_complement: bool = False) -> Iterator[Tile]:
        self._coordinates_on_board_check(row, col)
        for tile in self:
            is_central = (row, col) == (tile.row, tile.col)
            is_neighbour = (row - 1 <= tile.row <= row + 1) and (col - 1 <= tile.col <= col + 1)
            to_be_yielded = not is_neighbour if on_complement else is_neighbour
            if to_be_yielded and not is_central:
                yield tile

    