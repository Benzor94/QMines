

from enum import Enum
from typing import Final, override
from PySide6.QtCore import QSize, Slot, Signal, Qt
from PySide6.QtGui import QFont, QResizeEvent, QMouseEvent
from PySide6.QtWidgets import QPushButton, QSizePolicy

from qmines.symbols import TileSymbol, INDEX_MAP

Coordinates = tuple[int, int]

class TileState(Enum):
    INERT = 0  # The first click has not been made yet.
    ACTIVE = 1 # The game is ongoing.
    FINAL = 2  # The game has ended.

class MineCountChange(Enum):
    ADDED = 1
    REMOVED = -1


class Tile(QPushButton):

    MIN_SIZE: Final[int] = 25

    # Signal emitted when a mine is revealed; params are the coordinates of the triggering tile.
    mine_exploded = Signal(Coordinates)

    # Signal emitted when the tile is clicked for the first time in the game (among all tiles).
    # Params are the coordinates of the triggering tile.
    first_clicked = Signal(Coordinates)

    # Signal emitted when a tile that has already been revealed is clicked.
    revealed_tile_clicked = Signal(Coordinates)

    # Override of clicked signal; params are the coordinates of the triggering tile.
    clicked = Signal(Coordinates) # TODO: Probably no params needed, no override needed

    # Provide a signal for right clicks; params are the coordinates of the triggering tile.
    right_clicked = Signal(Coordinates) # TODO: Probably no params needed

    # Signal emitted when flat is set or removed.
    mine_count_change = Signal(MineCountChange)

    # Signal emitted when a non-mine tile is revealed; params are the coordinates of the triggering tile.
    tile_revealed = Signal(Coordinates)

    def __init__(self, coordinates: Coordinates = (0, 0)) -> None:
        super().__init__()
        self._is_mine: bool = False
        self._is_flagged: bool = False
        self._proximity: int = 0
        self._coordinates: Coordinates = coordinates
        self._state: TileState = TileState.INERT

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self._set_font_size(self.size().height())

        self.setCheckable(False)

    
    @property
    def is_mine(self) -> bool:
        return self._is_mine
    @is_mine.setter
    def is_mine(self, bool_: bool) -> None:
        self._is_mine = bool(bool_)

    @property
    def is_flagged(self) -> bool:
        return self._is_flagged

    @property
    def is_pressed(self) -> bool:
        return self.isDown()
    
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
    def coordinates(self) -> Coordinates:
        return self._coordinates
    
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
    def on_left_click(self) -> None:
        match self._state:
            case TileState.INERT:
                self._left_click_when_inert()
            case TileState.ACTIVE:
                if self.is_pressed:
                    self._left_click_when_active_and_pressed()
                else:
                    self._left_click_when_active_and_not_pressed()
            case TileState.FINAL:
                return

    @Slot()
    def on_right_click(self) -> None:
        if (self._state != TileState.ACTIVE) or (not self.is_pressed):
            return
        if self._is_flagged:
            self._is_flagged = False
            self._set_visual_state(TileSymbol.EMPTY)
            self.mine_count_change.emit(MineCountChange.REMOVED)
        else:
            self._is_flagged = True
            self._set_visual_state(TileSymbol.FLAG)
            self.mine_count_change.emit(MineCountChange.ADDED)

    @Slot()
    def on_game_over(self) -> None:
        if not self.is_pressed:
            symbol = TileSymbol.MINE if self.is_mine else TileSymbol(self.proximity)
            self._set_pressed()
            self._set_visual_state(symbol)
        self._state = TileState.FINAL
        self.setDisabled(True) # TODO: Since mouse events are overriden, check if disabled prevents signals.

    @Slot(Coordinates)
    def on_game_start(self, coords: Coordinates) -> None:
        self._state = TileState.ACTIVE
        if coords == self.coordinates:
            self.on_left_click()

    def _set_visual_state(self, symbol: TileSymbol):
        self.setText(INDEX_MAP[symbol.value])

    def _left_click_when_inert(self) -> None:
        self.first_clicked.emit(*self.coordinates)

    def _left_click_when_active_and_not_pressed(self) -> None:
        self._set_pressed()
        if self.is_mine:
            self._set_visual_state(TileSymbol.EXPLOSION)
            self.mine_exploded.emit(*self.coordinates)
        else:
            self._set_visual_state(TileSymbol(self.proximity))
            self.tile_revealed.emit(*self.coordinates)

    def _left_click_when_active_and_pressed(self) -> None:
        if not self.is_mine:
            self.revealed_tile_clicked.emit(*self.coordinates)

    def _set_pressed(self) -> None:
        self.setDown(True)





