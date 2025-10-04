from typing import override

from PySide6.QtCore import QSize
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QFrame, QGridLayout, QPushButton, QSizePolicy


class BoardView(QFrame):
    def __init__(self, height_to_width_ratio: float, tiles: dict[tuple[int, int], QPushButton]) -> None:
        super().__init__()
        self._height_to_width_ratio = height_to_width_ratio
        self._tiles = tiles
        self._layout = QGridLayout()
        self._set_size_properties()
        self._set_layout_properties()
        self._set_border()

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
        for (row, col), tile in self._tiles.items():
            self._layout.addWidget(tile, row, col)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

    def _set_border(self) -> None:
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(2)
