from collections.abc import Iterator
from random import sample
from threading import Lock

from PySide6.QtCore import QObject, Signal, Slot

from qmines.board.board_view import BoardView
from qmines.config import Config
from qmines.common import FlagCountChange
from qmines.tile.tile import Tile
from qmines.common import GameOverReason


class Board(QObject):
    flag_changed = Signal(FlagCountChange)
    game_over = Signal(GameOverReason)
    game_started = Signal()

    def __init__(self, config: Config) -> None:
        super().__init__()
        self._n_rows = config.number_of_rows
        self._n_cols = config.number_of_columns
        self._n_mines = config.number_of_mines
        self._size = self._n_rows * self._n_cols
        self._initialized = False
        self._game_over = False
        self._lock = Lock()
        self._revealed_tiles = 0
        self._tiles = {(row, col): self._create_tile(row, col) for row in range(self._n_rows) for col in range(self._n_cols)}
        self._view = BoardView(self._n_rows / self._n_cols, {coords: self._tiles[coords].view for coords in self._tiles})
        self.game_over.connect(self.on_game_over)

    def __getitem__(self, coordinates: tuple[int, int]) -> Tile:
        return self._tiles[coordinates]

    def __iter__(self) -> Iterator[Tile]:
        return iter(self._tiles.values())

    @property
    def view(self) -> BoardView:
        return self._view

    @Slot(int, int)
    def on_left_click(self, row: int, col: int) -> None:
        if self._game_over:
            return
        if not self._initialized:
            self._initialize_board(row, col)
        clicked_tile = self[row, col]
        if clicked_tile.is_flag:
            return
        if clicked_tile.is_revealed:
            nearby_flags = sum(1 for t in self._proximity_iterator(row, col) if t.is_flag)
            if clicked_tile.proximity_number == 0 or nearby_flags != clicked_tile.proximity_number:  # We proceed if revealed, but only if proximity number matches flags
                return
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

    @Slot()
    def on_game_over(self) -> None:
        self._game_over = True

    def _cascade_reveal(self, row: int, col: int) -> None:
        initial_tile = self[row, col]
        visited_tiles = {initial_tile}
        stack = [initial_tile]

        while stack:
            if self._game_over:
                break
            current = stack.pop()
            is_revealed = current.is_revealed
            self._handle_single_tile_reveal(current)
            if is_revealed or current.proximity_number == 0:
                for neighbour in (t for t in self._proximity_iterator(current.row, current.col) if not t.is_flag if not t.is_revealed if t not in visited_tiles):
                    stack.append(neighbour)
                    visited_tiles.add(neighbour)

    def _handle_single_tile_reveal(self, tile: Tile) -> None:
        if tile.is_mine:
            tile.exploded = True
            self.game_over.emit(GameOverReason.LOSS)
        elif not tile.is_revealed:
            tile.reveal()
            self._register_revealed_tile()

    def _initialize_board(self, row: int, col: int) -> None:
        tile_pool = [tile for tile in self if not tile.is_neighbour(self[row, col])]
        mines = sample(tile_pool, self._n_mines)
        for tile in mines:
            tile.is_mine = True
        for tile in (t for t in self if not t.is_mine):
            tile.proximity_number = sum(1 for t in self._proximity_iterator(tile.row, tile.col) if t.is_mine)
        self._initialized = True
        self.game_started.emit()
        self.on_left_click(row, col)

    def _create_tile(self, row: int, col: int) -> Tile:
        tile = Tile(row, col)
        tile.left_clicked.connect(self.on_left_click)
        tile.right_clicked.connect(self.on_right_click)
        self.game_over.connect(tile.on_game_over)
        return tile

    def _register_revealed_tile(self) -> None:
        if self._game_over:
            return
        with self._lock:
            self._revealed_tiles += 1
            if self._size - self._revealed_tiles == self._n_mines:
                self.game_over.emit(GameOverReason.WIN)

    def _coordinates_on_board(self, row: int, col: int) -> bool:
        return (0 <= row < self._n_rows) and (0 <= col < self._n_cols)

    def _proximity_iterator(self, row: int, col: int) -> Iterator[Tile]:
        if not self._coordinates_on_board(row, col):
            raise ValueError(f'Coordinates ({row}, {col}) are not on the board.')
        for r in (row - 1, row, row + 1):
            for c in (col - 1, col, col + 1):
                if self._coordinates_on_board(r, c) and not (r == row and c == col):
                    yield self[r, c]
