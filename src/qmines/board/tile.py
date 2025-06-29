from enum import Enum
from typing import Final, override
import PySide6.QtWidgets as QW
import PySide6.QtCore as QC
import PySide6.QtGui as QG
from PySide6.QtCore import Signal

from qmines.utilities import set_font_size_based_on_height
from qmines.utilities.constants import Symbol
from qmines.state_processor import StateProcessor, State

class MineCountChange(Enum):
    ADDED = 1
    REMOVED = -1

class Tile(QW.QPushButton):
    MIN_SIZE: Final[int] = 32

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
        self._is_revealed = False
        self._proximity_number = -1
        self._signal_node = StateProcessor()

        self.setSizePolicy(QW.QSizePolicy.Policy.Minimum, QW.QSizePolicy.Policy.Minimum)
        set_font_size_based_on_height(self, self.size().height())
        self.left_clicked.connect(self.on_left_click)
        self.right_clicked.connect(self.on_right_click)
    
    @property
    def coordinates(self) -> tuple[int, int]:
        return self._coordinates
    
    @property
    def is_mine(self) -> bool:
        return self._is_mine
    @is_mine.setter
    def is_mine(self, value: bool) -> None:
        self._is_mine = bool(value)
    
    @property
    def proximity_number(self) -> int:
        return self._proximity_number
    @proximity_number.setter
    def proximity_number(self, value: int) -> None:
        if not (0 <= value <= 8):
            raise ValueError(f'Attempted to set an integer outside the range [0, 8] on tile {self._coordinates}')
        self._proximity_number = value
    
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
            self.setDown(False)
        elif e.button() == QC.Qt.MouseButton.RightButton:
            self.right_clicked.emit()

    @QC.Slot()
    def on_left_click(self) -> None:
        match self._signal_node.state:
            case State.INACTIVE:
                self.first_click_in_game.emit(*self.coordinates)
            case State.ACTIVE:
                if not self._is_revealed:
                    self._on_left_click_when_unrevealed()
                else:
                    ...
            case State.PAUSED | State.WIN | State.LOSS_MINE_HIT | State.LOSS_TIMEOUT:
                return

    @QC.Slot()
    def on_right_click(self) -> None:
        ...

    @QC.Slot(int, int)
    def on_game_start(self, i: int, j: int) -> None:
        if (i, j) == self._coordinates:
            self.on_left_click()
    
    def _on_left_click_when_unrevealed(self) -> None:
        self.setFlat(True)
        self._is_revealed = True
        self._set_text_on_reveal_by_left_click()
        self.tile_revealed.emit(*self.coordinates, self._is_mine)
    
    def _set_text_on_reveal_by_left_click(self) -> None:
        if self._is_mine:
            self.setText(Symbol.EXPLOSION.value)
        else:
            self.setText(str(self._proximity_number))