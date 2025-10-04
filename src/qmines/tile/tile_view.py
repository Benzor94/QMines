from enum import Enum
from pathlib import Path
from typing import Final, override

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QFont, QIcon, QMouseEvent, QResizeEvent
from PySide6.QtWidgets import QPushButton, QSizePolicy

from qmines.common import get_qicon_from_path, get_resources_dir

type DisplayState = TileView.IconState | int


class TileView(QPushButton):

    class IconState(Enum):
        EMPTY = 0
        FLAG = 1
        MINE = 2
        EXPLOSION = 3
    
    class PressedState(Enum):
        RAISED = 0
        FLAT = 1
        HIDDEN = 2

    MIN_SIZE: Final[int] = 32

    MINE_ICON: Final[Path] = get_resources_dir() / 'mine256.png'
    FLAG_ICON: Final[Path] = get_resources_dir() / 'flag256.png'
    BOOM_ICON: Final[Path] = get_resources_dir() / 'explosion256.png'

    left_clicked = Signal()
    right_clicked = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._set_size_properties()
        self._empty_icon = QIcon('')
        self._flag_icon = get_qicon_from_path(self.FLAG_ICON)
        self._mine_icon = get_qicon_from_path(self.MINE_ICON)
        self._boom_icon = get_qicon_from_path(self.BOOM_ICON)

    def set_display_state(self, state: DisplayState) -> None:
        match state:
            case self.IconState() as icon_state:
                match icon_state:
                    case self.IconState.EMPTY:
                        icon = self._empty_icon
                    case self.IconState.FLAG:
                        icon = self._flag_icon
                    case self.IconState.MINE:
                        icon = self._mine_icon
                    case self.IconState.EXPLOSION:
                        icon = self._boom_icon
                self._set_icon(icon)
            case int() as int_state:
                if int_state == 0:
                    txt = ''
                elif 0 < int_state <= 8:
                    txt = str(int_state)
                else:
                    raise ValueError(f'Can display only integers 0 - 8 on tile, attempted to display {int_state}.')
                self._set_text(txt)

    def set_pressed_state(self, state: PressedState) -> None:
        match state:
            case self.PressedState.RAISED:
                self.setVisible(True)
                self.setFlat(False)
                self.setDown(False)
            case self.PressedState.FLAT:
                self.setVisible(True)
                self.setFlat(True)
                self.setDown(False)
            case self.PressedState.HIDDEN:
                self.setVisible(False)

    @override
    def sizeHint(self) -> QSize:
        return QSize(self.MIN_SIZE, self.MIN_SIZE)

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        new_height = event.size().height()
        self._set_font_size_based_on_height(new_height)
        self._adjust_icon_size(new_height)

    @override
    def mouseReleaseEvent(self, e: QMouseEvent, /):
        if e.button() == Qt.MouseButton.LeftButton:
            self.setDown(False)
            self.left_clicked.emit()
        elif e.button() == Qt.MouseButton.RightButton:
            self.right_clicked.emit()

    def _set_size_properties(self) -> None:
        size_policy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        size_policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(size_policy)
        self._set_font_size_based_on_height(self.size().height())
        self._adjust_icon_size(self.size().height())

    def _set_text(self, txt: str) -> None:
        self.setIcon(QIcon())
        self.setText(txt)

    def _set_icon(self, icon: QIcon) -> None:
        self.setText('')
        self.setIcon(icon)

    def _adjust_icon_size(self, height: int) -> None:
        self.setIconSize(QSize(height - 2, height - 2)) if height > 2 else self.setIconSize(QSize(height, height))
    
    def _set_font_size_based_on_height(self, height: int) -> None:
        new_size = height // 2
        current_font = self.font()
        if current_font.pointSize() != new_size:
            self.setFont(QFont(current_font.family(), new_size))
