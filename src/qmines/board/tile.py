from typing import Final, override

from PySide6.QtCore import QSize, Qt, Signal, Slot
from PySide6.QtGui import QMouseEvent, QResizeEvent
from PySide6.QtWidgets import QPushButton, QSizePolicy

from qmines.constants import Symbol
from qmines.state.state_manager import FlagCountChange, State, StateManager
from qmines.utilities import set_font_size_based_on_height


class Tile(QPushButton):
    MIN_SIZE: Final[int] = 32

    left_clicked = Signal()
    right_clicked = Signal()

    def __init__(self, coordinates: tuple[int, int]) -> None:
        super().__init__()
        self._coordinates = coordinates
        self._is_mine = False
        self._is_flagged = False
        self._is_revealed = False
        self._is_the_first_clicked_tile = False
        self._proximity_number = -1
        self._state_manager = StateManager()
        self._set_size_properties()
        self._set_up_connections()

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
    def is_flagged(self) -> bool:
        return self._is_flagged

    @property
    def is_revealed(self) -> bool:
        return self._is_revealed

    @property
    def proximity_number(self) -> int:
        return self._proximity_number

    @proximity_number.setter
    def proximity_number(self, value: int) -> None:
        self._proximity_number = value

    @Slot()
    def on_left_click(self) -> None:
        match self._state_manager.state:
            case State.INACTIVE:
                self._is_the_first_clicked_tile = True
                self._state_manager.first_click_in_game.emit(*self.coordinates)
            case State.ACTIVE:
                if self._is_flagged:
                    return
                if self._is_revealed:
                    self._state_manager.revealed_tile_clicked.emit(*self.coordinates)
                else:
                    self._reveal_tile()
            case _:
                return

    @Slot()
    def on_right_click(self) -> None:
        match self._state_manager.state:
            case State.ACTIVE:
                if self._is_revealed:
                    return
                if self._is_flagged:
                    self._set_text_on_flag(False)
                    self._is_flagged = False
                    self._state_manager.flag_count_change.emit(FlagCountChange.REMOVED)
                else:
                    self._set_text_on_flag(True)
                    self._is_flagged = True
                    self._state_manager.flag_count_change.emit(FlagCountChange.ADDED)
            case _:
                return

    @Slot(State, State)
    def on_state_change(self, previous: State, current: State) -> None:
        if self._is_revealed:
            return
        match current:
            case State.ACTIVE:
                if previous == State.INACTIVE and self._is_the_first_clicked_tile:
                    self.on_left_click()
            case State.WIN:
                self._set_text_on_reveal(mine_symbol=Symbol.FLAG)
                self.setFlat(True)
            case State.LOSS_MINE_HIT:
                self._set_text_on_reveal(mine_symbol=Symbol.MINE)
                self.setFlat(True)
            case State.LOSS_TIMEOUT:
                self._set_text_on_reveal(mine_symbol=Symbol.EXPLOSION)
                self.setFlat(True)
            case _:
                return

    @override
    def sizeHint(self) -> QSize:
        return QSize(self.MIN_SIZE, self.MIN_SIZE)

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        new_height = event.size().height()
        set_font_size_based_on_height(self, new_height)

    @override
    def mouseReleaseEvent(self, e: QMouseEvent, /):
        if e.button() == Qt.MouseButton.LeftButton:
            self.left_clicked.emit()
            self.setDown(False)
        elif e.button() == Qt.MouseButton.RightButton:
            self.right_clicked.emit()

    def _set_size_properties(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        set_font_size_based_on_height(self, self.size().height())

    def _reveal_tile(self) -> None:
        self.setFlat(True)
        self._is_revealed = True
        self._set_text_on_reveal()
        if self.is_mine:
            self._state_manager.state = State.LOSS_MINE_HIT
        self._state_manager.tile_revealed.emit(*self.coordinates)

    def _set_text_on_reveal(self, *, mine_symbol: Symbol = Symbol.EXPLOSION) -> None:
        if self._is_mine:
            self.setText(mine_symbol.value)
        else:
            self.setText(str(self._proximity_number)) if self._proximity_number else None

    def _set_text_on_flag(self, flagged: bool) -> None:
        if flagged:
            self.setText(Symbol.FLAG.value)
        else:
            self.setText('')

    def _set_up_connections(self) -> None:
        self.left_clicked.connect(self.on_left_click)
        self.right_clicked.connect(self.on_right_click)
        self._state_manager.state_change.connect(self.on_state_change)
