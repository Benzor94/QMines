

from enum import Enum
from typing import Final, override
from PySide6.QtCore import QSize
from PySide6.QtGui import QFont, QResizeEvent
from PySide6.QtWidgets import QPushButton, QSizePolicy

class TileVisualState(Enum):
    EMPTY = 0
    FLAGGED = 1
    REVEALED = 2

class Tile(QPushButton):

    MIN_SIZE: Final[int] = 25
    MINE_CHAR = '\U0001F4A3'
    FLAG_CHAR = '\U0001F6A9'

    def __init__(self) -> None:
        super().__init__()
        self._is_mine: bool = False
        self._visual_state: TileVisualState = TileVisualState.EMPTY
        self._proximity: int = 0
        self._coordinates: tuple[int, int] = (0, 0)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self._set_font_size(self.size().height())

        # This is only for testing
        self.setCheckable(True)
        self.clicked.connect(self.on_click)

    
    @property
    def is_mine(self) -> bool:
        return self._is_mine
    @is_mine.setter
    def is_mine(self, bool_: bool) -> None:
        self._is_mine = bool(bool_)
    
    @property
    def visual_state(self) -> TileVisualState:
        return self._visual_state
    
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
    def coordinates(self, i: int, j: int) -> None:
        # Validity check must be performed by the caller.
        self._coordinates = (i, j)
    
    @override
    def sizeHint(self) -> QSize:
        return QSize(self.__class__.MIN_SIZE, self.__class__.MIN_SIZE)
    
    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        new_height = event.size().height()
        self._set_font_size(new_height)
    
    def on_click(self) -> None:
        self.setText(self.__class__.MINE_CHAR)
        self.setChecked(True)
        self.setDisabled(True)

    def _set_font_size(self, height: int) -> None:
        new_size = height // 2
        current_font = self.font()
        if current_font.pointSize() != new_size:
            self.setFont(QFont(current_font.family(), new_size))

