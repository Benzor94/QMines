

from collections.abc import Iterator, Sequence
from typing import override
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QFrame, QGridLayout, QSizePolicy

from qmines.board.board_tile import Tile
from qmines.game_parameters import GameParameters


class Board(QFrame):

    def __init__(self, parameters: GameParameters, tiles: Sequence[Tile]) -> None:
        super().__init__()
        self._params = parameters
        self._tiles = tuple(tiles)
        self._verify_tile_count_validity()
        self._set_size_properties()
        self._board_layout = QGridLayout()
        self._set_layout_properties()
    
    @property
    def n_rows(self) -> int:
        return self._params.n_rows
    @property
    def n_cols(self) -> int:
        return self._params.n_cols
    @property
    def n_tiles(self) -> int:
        return self._params.size
    
    def __getitem__(self, key: int | tuple[int, int]) -> Tile:
        if not isinstance(key, int):
            i, j = key
            idx = self._params.to_index(i, j)
        else:
            idx = int(key)
        return self._tiles[idx]
    
    def __iter__(self) -> Iterator[Tile]:
        return iter(self._tiles)
    
    def proximity_iterator(self, idx1: int, idx2: int | None) -> Iterator[Tile]:
        if idx2 is None:
            i, j = self._params.to_coordinates(idx1)
        else:
            i, j =  self._params.wrap_coordinates(idx1, idx2)
        for k in (i - 1, i, i + 1):
            for l in (j - 1, j, j + 1):
                if self._coordinates_represent_valid_proximity(k, l, (i, j)):
                    yield self[k, l]      

    @override
    def resizeEvent(self, event: QResizeEvent):
        size = event.size()
        height = size.height()
        width = size.width()
        smallest = min(height, width)
        self.resize(QSize(smallest, smallest))
    
    def _verify_tile_count_validity(self) -> None:
        if len(self._tiles) != self.n_tiles:
            raise ValueError(f'The number of tiles in the board object ({len(self._tiles)}) must agree with'
                             f'the number of tiles in the parameters object ({self.n_tiles}).')
    
    def _coordinates_represent_valid_proximity(self, i: int, j: int, center_crds: tuple[int, int]) -> bool:
        i_is_on_board = 0 <= i < self.n_rows
        j_is_on_board = 0 <= j < self.n_cols
        crds_are_not_central = (i, j) != center_crds
        return i_is_on_board and j_is_on_board and crds_are_not_central

    def _set_size_properties(self) -> None:
        self.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)
        size_policy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        size_policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(size_policy)
    
    def _set_layout_properties(self) -> None:
        for tile in self:
            self._board_layout.addWidget(tile, tile.coordinates[0], tile.coordinates[1])
        self._board_layout.setSpacing(0)
        self._board_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._board_layout)

