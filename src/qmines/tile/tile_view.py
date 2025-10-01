from pathlib import Path
from typing import Final, override

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon, QMouseEvent, QResizeEvent
from PySide6.QtWidgets import QPushButton, QSizePolicy

from qmines.enums import IconState, PressedState
from qmines.utilities import get_qicon_from_path, get_resources_dir, set_font_size_based_on_height

type DisplayState = IconState | int


class TileView(QPushButton):
    MIN_SIZE: Final[int] = 32

    MINE_ICON: Final[Path] = get_resources_dir() / 'mine256.png'
    FLAG_ICON: Final[Path] = get_resources_dir() / 'flag256.png'
    BOOM_ICON: Final[Path] = get_resources_dir() / 'explosion256.png'

    left_clicked = Signal()
    right_clicked = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._set_size_properties()

    def set_display_state(self, state: DisplayState) -> None:
        match state:
            case IconState() as icon_state:
                match icon_state:
                    case IconState.EMPTY:
                        icon = QIcon('')
                    case IconState.FLAG:
                        icon = get_qicon_from_path(self.FLAG_ICON)
                    case IconState.MINE:
                        icon = get_qicon_from_path(self.MINE_ICON)
                    case IconState.EXPLOSION:
                        icon = get_qicon_from_path(self.BOOM_ICON)
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
            case PressedState.RAISED:
                self.setVisible(True)
                self.setFlat(False)
                self.setDown(False)
            case PressedState.FLAT:
                self.setVisible(True)
                self.setFlat(True)
                self.setDown(False)
            case PressedState.HIDDEN:
                self.setVisible(False)

    @override
    def sizeHint(self) -> QSize:
        return QSize(self.MIN_SIZE, self.MIN_SIZE)

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        new_height = event.size().height()
        set_font_size_based_on_height(self, new_height)
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
        set_font_size_based_on_height(self, self.size().height())
        self._adjust_icon_size(self.size().height())

    def _set_text(self, txt: str) -> None:
        self.setIcon(QIcon())
        self.setText(txt)

    def _set_icon(self, icon: QIcon) -> None:
        self.setText('')
        self.setIcon(icon)

    def _adjust_icon_size(self, height: int) -> None:
        self.setIconSize(QSize(height - 2, height - 2)) if height > 2 else self.setIconSize(QSize(height, height))
