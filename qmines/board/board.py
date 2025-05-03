

from collections.abc import Iterator
from typing import override
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QFrame, QGridLayout, QSizePolicy

from qmines.board.board_tile import Tile
from qmines.game_parameters import GameParameters


class Board(QFrame):

    def __init__(self, parameters: GameParameters) -> None:
        super().__init__()
        self._params = parameters
        self._tiles = self._generate_tiles()
        self.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        # self.setSizePolicy()
        self.board_layout = QGridLayout()
        for tile in self:
            self.board_layout.addWidget(tile, *tile.coordinates)
        self.board_layout.setSpacing(0)
        self.board_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.board_layout)
    
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
    
    def _generate_tiles(self) -> list[Tile]:
        idx_to_crds = self._params.to_coordinates
        return [Tile(idx_to_crds(idx)) for idx in range(self.n_tiles)]
    
    def _coordinates_represent_valid_proximity(self, i: int, j: int, center_crds: tuple[int, int]) -> bool:
        i_is_on_board = 0 <= i < self.n_rows
        j_is_on_board = 0 <= j < self.n_cols
        crds_are_not_central = (i, j) != center_crds
        return i_is_on_board and j_is_on_board and crds_are_not_central

