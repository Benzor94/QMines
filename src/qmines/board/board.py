from collections.abc import Iterator
from random import sample
from threading import Lock

from PySide6.QtCore import QObject, Signal, Slot

from qmines.board.board_view import BoardView
from qmines.config import Config
from qmines.enums import FlagCountChange, GameOverReason
from qmines.tile.tile import Tile
from qmines.tile.tile_icons import TileIconRepository


class Board(QObject):
    flag_changed = Signal(FlagCountChange)
    game_over = Signal(GameOverReason)
    trigger_tile = Signal(int, int)
    game_started = Signal()

    def __init__(self, config: Config) -> None:
        super().__init__()
        self._n_rows = config.number_of_rows
        self._n_cols = config.number_of_columns
        self._n_mines = config.number_of_mines
        self._size = self._n_rows * self._n_cols
        self._icons = TileIconRepository()
        self._initialized = False
        self._game_over = False
        self._revealed_tiles = 0
        self._lock = Lock()
        self._tiles = [self._create_tile(idx) for idx in range(self._size)]
        self._view = BoardView(self._n_rows / self._n_cols, {(t.row, t.col): t.view for t in self._tiles})
        self.trigger_tile.connect(self.on_left_click)

    def __getitem__(self, coordinates: tuple[int, int]) -> Tile:
        return self._tiles[self._coordinates_to_index(*coordinates)]

    def __iter__(self) -> Iterator[Tile]:
        return iter(self._tiles)

    def __del__(self) -> None:
        print('Board was deleted.')

    @property
    def view(self) -> BoardView:
        return self._view

    @Slot(int, int)
    def on_left_click(self, row: int, col: int) -> None:
        if self._game_over:
            return
        if not self._initialized:
            self._set_up_board(row, col)
            self._initialized = True
            self.trigger_tile.emit(row, col)
            self.game_started.emit()
            return
        clicked_tile = self[row, col]
        if clicked_tile.is_flag:
            return
        if clicked_tile.is_revealed and clicked_tile.proximity_number != 0 and not clicked_tile.is_mine:
            number_of_nearby_flags = sum(1 for tile in self._proximity_iterator(row, col) if tile.is_flag)
            if number_of_nearby_flags == clicked_tile.proximity_number:
                self._cascade_reveal(row, col)
            return
        if not clicked_tile.is_revealed:
            self._reveal_tile(clicked_tile)
            if clicked_tile.proximity_number == 0:
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
            self.flag_changed.emit(FlagCountChange.REMOVED)
        else:
            tile.set_flag(True)
            self.flag_changed.emit(FlagCountChange.ADDED)

    def _create_tile(self, idx: int) -> Tile:
        tile = Tile(*self._index_to_coordinates(idx), self._icons)
        tile.left_clicked.connect(self.on_left_click)
        tile.right_clicked.connect(self.on_right_click)
        return tile

    def _reveal_tile(self, tile: Tile) -> None:
        if tile.is_mine:
            tile.exploded = True
            self._reveal_all_tiles()
            self._game_over = True
            self.game_over.emit(GameOverReason.LOSS)
        else:
            tile.reveal()
            self._register_revealed_tile()

    def _reveal_all_tiles(self) -> None:
        for tile in self:
            tile.reveal()

    def _cascade_reveal(self, row: int, col: int) -> None:
        for neighbour in (t for t in self._proximity_iterator(row, col) if not t.is_revealed):
            self.trigger_tile.emit(neighbour.row, neighbour.col)

    def _register_revealed_tile(self) -> None:
        with self._lock:
            self._revealed_tiles += 1
            if self._size - self._revealed_tiles == self._n_mines:
                self._reveal_all_tiles()
                self._game_over = True
                self.game_over.emit(GameOverReason.WIN)

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
        match on_complement:
            case True:
                return self._proximity_iterator_inverse(row, col)
            case False:
                return self._proximity_iterator_direct(row, col)

    def _proximity_iterator_direct(self, row: int, col: int) -> Iterator[Tile]:
        for r in (row - 1, row, row + 1):
            for c in (col - 1, col, col + 1):
                if self._is_on_board(r, c) and not (r == row and c == col):
                    yield self[r, c]

    def _proximity_iterator_inverse(self, row: int, col: int) -> Iterator[Tile]:
        for r in set(range(self._n_rows)) - {row - 1, row, row + 1}:
            for c in set(range(self._n_cols)) - {col - 1, col, col + 1}:
                yield self[r, c]
