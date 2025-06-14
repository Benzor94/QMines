from enum import Enum
from typing import Final, override
import PySide6.QtWidgets as QW
import PySide6.QtCore as QC
import PySide6.QtGui as QG
from PySide6.QtCore import Signal

from qmines.utilities import set_font_size_based_on_height
from qmines.global_state import StateTracker

class MineCountChange(Enum):
    ADDED = 1
    REMOVED = -1

class Tile(QW.QPushButton):
    MIN_SIZE: Final[int] = 30

    left_clicked = Signal()
    right_clicked = Signal()

    first_click_in_game = Signal(int, int)
    tile_revealed = Signal(int, int, bool)
    revealed_tile_clicked = Signal(int, int)

    mine_count_change = Signal(MineCountChange)

    def __init__(self, coordinates: tuple[int, int] = (0, 0)) -> None:
        super().__init__()
        self._coordinates = coordinates
        self._is_mine = False
        self._is_flagged = False

        self.setSizePolicy(QW.QSizePolicy.Policy.Minimum, QW.QSizePolicy.Policy.Minimum)
        set_font_size_based_on_height(self, self.size().height())
        self.left_clicked.connect(self.on_left_click)
        self.right_clicked.connect(self.on_right_click)
    
    @property
    def coordinates(self) -> tuple[int, int]:
        return self._coordinates
    
    @override
    def sizeHint(self) -> QC.QSize:
        return QC.QSize(self.__class__.MIN_SIZE, self.__class__.MIN_SIZE)
    
    @override
    def resizeEvent(self, event: QG.QResizeEvent) -> None:
        new_height = event.size().height()
        set_font_size_based_on_height(self, new_height)

    @override
    def mouseReleaseEvent(self, e: QG.QMouseEvent, /):
        if e.button() == QC.Qt.MouseButton.LeftButton:
            self.left_clicked.emit()
        elif e.button() == QC.Qt.MouseButton.RightButton:
            self.right_clicked.emit()

    @QC.Slot()
    def on_left_click(self) -> None:
        if not StateTracker.game_is_active:
            self.first_click_in_game.emit(*self.coordinates)
            self.setDown(False)
        elif not self.isDown():
            self.setDown(True)
            self.tile_revealed.emit(*self.coordinates, self._is_mine)
        else:
            ...

    @QC.Slot()
    def on_right_click(self) -> None:
        ...

    @QC.Slot(int, int)
    def on_game_start(self, i: int, j: int) -> None:
        if (i, j) == self._coordinates:
            self.on_left_click()