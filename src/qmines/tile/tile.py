
from PySide6.QtCore import QObject, Signal, Slot

from qmines.enums import IconState, PressedState
from qmines.tile.tile_icons import TileIconRepository
from qmines.tile.tile_view import TileView


class Tile(QObject):
    left_clicked = Signal(int, int)
    right_clicked = Signal(int, int)

    def __init__(self, row: int, col: int, icons: TileIconRepository) -> None:
        super().__init__()
        self._row = row
        self._col = col
        self._is_revealed = False
        self._is_flag = False
        self._is_mine = False
        self._proximity_number = -1
        self._exploded = False
        self._view = TileView(icons)
        self.view.left_clicked.connect(self.on_left_click)
        self.view.right_clicked.connect(self.on_right_click)

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col

    @property
    def view(self) -> TileView:
        return self._view

    @property
    def is_revealed(self) -> bool:
        return self._is_revealed

    @property
    def is_flag(self) -> bool:
        return self._is_flag

    @property
    def is_mine(self) -> bool:
        return self._is_mine

    @is_mine.setter
    def is_mine(self, value: bool) -> None:
        self._is_mine = value

    @property
    def proximity_number(self) -> int:
        return self._proximity_number

    @proximity_number.setter
    def proximity_number(self, value: int) -> None:
        if 0 <= value <= 8:
            self._proximity_number = value
            return
        raise ValueError(f'Proximity number must be between 0 and 8 (inclusive). It was {value}.')

    @property
    def exploded(self) -> bool:
        return self._exploded

    @exploded.setter
    def exploded(self, value: bool) -> None:
        self._exploded = value

    @Slot()
    def on_left_click(self) -> None:
        self.left_clicked.emit(self.row, self.col)

    @Slot()
    def on_right_click(self) -> None:
        self.right_clicked.emit(self.row, self.col)

    def set_flag(self, flag: bool) -> None:
        self._is_flag = flag
        if flag:
            self.view.set_display_state(IconState.FLAG)
        else:
            self.view.set_display_state(IconState.EMPTY)

    def reveal(self) -> None:
        self._is_revealed = True
        if self.exploded:
            self.view.set_display_state(IconState.EXPLOSION)
            self.view.set_pressed_state(PressedState.FLAT)
        elif self.is_mine:
            self.view.set_display_state(IconState.MINE)
            self.view.set_pressed_state(PressedState.FLAT)
        else:
            self.view.set_display_state(self.proximity_number)
            self.view.set_pressed_state(PressedState.HIDDEN if self.proximity_number == 0 else PressedState.FLAT)
        
