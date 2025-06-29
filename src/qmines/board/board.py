from collections.abc import Iterator, Sequence
from typing import override

import PySide6.QtWidgets as QW
import PySide6.QtCore as QC
import PySide6.QtGui as QG

from qmines.board.tile import Tile
from qmines.game_parameters.game_parameters import GameParameters
from qmines.state_processor import StateProcessor
from qmines.utilities.index_tools import convert_coordinates_to_index


class Board(QW.QFrame):

    def __init__(self, tiles: Sequence[Tile]) -> None:
        super().__init__()
        self._parameters = StateProcessor().parameters
        self._h_to_w_ratio = self._parameters.n_rows / self._parameters.n_cols
        self._tiles = tiles
        self._layout = QW.QGridLayout()
        self._set_size_properties()
        self._set_layout_properties()
    
    @property
    def n_rows(self) -> int:
        return self._parameters.n_rows
    
    @property
    def n_cols(self) -> int:
        return self._parameters.n_cols

    def __getitem__(self, coordinates: tuple[int, int]) -> Tile:
        idx = convert_coordinates_to_index(*coordinates, self.n_rows, self.n_cols)
        return self._tiles[idx]

    def __iter__(self) -> Iterator[Tile]:
        return iter(self._tiles)
    
    @override
    def resizeEvent(self, event: QG.QResizeEvent):
        size = event.size()
        height = size.height()
        width = size.width()
        if height <= width * self._h_to_w_ratio:
            self.resize(QC.QSize(round(height / self._h_to_w_ratio), height))
        else:
            self.resize(QC.QSize(width, round(width * self._h_to_w_ratio)))
    
    def _set_size_properties(self) -> None:
        self.setAttribute(QC.Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)
        size_policy = QW.QSizePolicy(QW.QSizePolicy.Policy.Minimum, QW.QSizePolicy.Policy.Minimum)
        size_policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(size_policy)
    
    def _set_layout_properties(self) -> None:
        for tile in self:
            self._layout.addWidget(tile, tile.coordinates[0], tile.coordinates[1])
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)