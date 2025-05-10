

from enum import Enum
from typing import Final, override
from PySide6.QtCore import QSize, Slot, Signal, Qt
from PySide6.QtGui import QFont, QResizeEvent, QMouseEvent
from PySide6.QtWidgets import QPushButton, QSizePolicy

from qmines.symbols import Symbols

class TileState(Enum):
    INERT = 0  # The first click has not been made yet.
    ACTIVE = 1 # The game is ongoing.
    GAME_OVER = 2  # The game has ended.


class MineCountChange(Enum):
    ADDED = 1
    REMOVED = -1

class Tile(QPushButton):

    MIN_SIZE: Final[int] = 25

    # Signal emitted when a mine is revealed; params are the coordinates of the triggering tile.
    mine_exploded = Signal(int, int)

    # Signal emitted when the tile is clicked for the first time in the game (among all tiles).
    # Params are the coordinates of the triggering tile.
    first_clicked = Signal(int, int)

    # Override of clicked signal; params are the coordinates of the triggering tile.
    clicked = Signal(int, int)

    # Provide a signal for right clicks; params are the coordinates of the triggering tile.
    right_clicked = Signal(int, int)

    # Signal emitted when flat is set or removed.
    mine_count_change = Signal(MineCountChange)

    # Signal emitted when a tile is revealed.
    tile_revealed = Signal()

    def __init__(self, coordinates: tuple[int, int] = (0, 0)) -> None:
        super().__init__()
        self._is_mine: bool = False
        self._is_flagged: bool = False
        self._proximity: int = 0
        self._coordinates: tuple[int, int] = coordinates

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self._set_font_size(self.size().height())

        self.setCheckable(False)
        self._is_game_over = True

    
    @property
    def is_mine(self) -> bool:
        return self._is_mine
    @is_mine.setter
    def is_mine(self, bool_: bool) -> None:
        self._is_mine = bool(bool_)
    
    @property
    def proximity(self) -> int:
        return self._proximity
    @proximity.setter
    def proximity(self, mines_nearby: int) -> None:
        mines_nearby = int(mines_nearby)
        if mines_nearby < 0 or mines_nearby > 8:
            raise ValueError(f'The possible number of neighbouring mines {mines_nearby} must be between 0 and 8 (inclusive).')
        self._proximity = mines_nearby
    
    @property
    def coordinates(self) -> tuple[int, int]:
        return self._coordinates
    @coordinates.setter
    def coordinates(self, coords: tuple[int, int]) -> None:
        # Validity check must be performed by the caller.
        self._coordinates = coords
    
    @override
    def sizeHint(self) -> QSize:
        return QSize(self.__class__.MIN_SIZE, self.__class__.MIN_SIZE)
    
    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        new_height = event.size().height()
        self._set_font_size(new_height)

    def _set_font_size(self, height: int) -> None:
        new_size = height // 2
        current_font = self.font()
        if current_font.pointSize() != new_size:
            self.setFont(QFont(current_font.family(), new_size))

    @override
    def mouseReleaseEvent(self, e: QMouseEvent, /):
        if e.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        elif e.button() == Qt.MouseButton.RightButton:
            self.right_clicked.emit()

    @Slot()
    def on_checked(self) -> None:
        if not self._is_game_over:
            self.setCheckable(False)
            if self.is_mine:
                self.setText(Symbols.EXPLOSION.value)
                self.mine_exploded.emit(*self.coordinates)
            elif self.proximity > 0:
                self.setText(str(self.proximity))

    @Slot()
    def on_right_click(self) -> None:
        if not self.isChecked():
            match self._is_flagged:
                case True:
                    self.setText('')
                    self._is_flagged = False
                    self.setCheckable(True)

    @Slot()
    def on_game_over(self) -> None:
        self._is_game_over = True
        if not self.isChecked():
            self._is_game_over = False

    def _set_visual_state(self): ...




