from pathlib import Path
from typing import Final

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLCDNumber

from qmines.utilities import get_qicon_from_path, get_resources_dir


class MineCounter(QFrame):

    ICON: Final[Path] = get_resources_dir() / 'mine256.png'
    ICON_SIZE: Final[int] = 20

    def __init__(self, n_mines: int) -> None:
        super().__init__()
        self._n_mines = n_mines
        self._label = QLabel()
        self._separator = QLabel(':')
        self._counter = QLCDNumber()
        self._layout = QHBoxLayout()
        self._label.setPixmap(get_qicon_from_path(self.ICON).pixmap(self.ICON_SIZE, self.ICON_SIZE))
        self.setToolTip('Number of mines remaining')
        self._set_counter_properties()
        self._set_layout_properties()
    
    def _set_counter_properties(self) -> None:
        init_number = str(self._n_mines)
        self._counter.setDigitCount(len(init_number))
        self._counter.display(init_number)
        self._counter.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self._counter.setStyleSheet("QLCDNumber {background-color: black; color: red; }")
    
    def _set_layout_properties(self) -> None:
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._separator)
        self._layout.addWidget(self._counter)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
    
    def update_counter(self, value: int) -> None:
        value_str = str(value)
        digits = len(value_str)
        self._counter.setDigitCount(digits)
        self._counter.display(value_str)

class TimeTracker(QFrame):

    ICON: Final[Path] = get_resources_dir() / 'clock16.png'
    ICON_SIZE: Final[int] = 20

    def __init__(self) -> None:
        super().__init__()
        self._label = QLabel()
        self._separator = QLabel(':')
        self._counter = QLCDNumber()
        self._layout = QHBoxLayout()
        self._label.setPixmap(get_qicon_from_path(self.ICON).pixmap(self.ICON_SIZE, self.ICON_SIZE))
        self.setToolTip('Seconds elapsed')
        self._set_counter_properties()
        self._set_layout_properties()        
    
    def _set_counter_properties(self) -> None:
        self._counter.setDigitCount(1)
        self._counter.display('0')
        self._counter.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self._counter.setStyleSheet("QLCDNumber { background-color: black; color: red; }")
    
    def _set_layout_properties(self) -> None:        
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._separator)
        self._layout.addWidget(self._counter)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
    
    def update_counter(self, value: int) -> None:
        value_str = str(value)
        digits = min(len(value_str), 4)
        self._counter.setDigitCount(digits)
        self._counter.display(value_str if len(value_str) <= 4 else '9999')
