from enum import Enum

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QPushButton


class ModeSelectorButton(QPushButton):

    class Mode(Enum):
        EASY = 'Easy\n(8 x 8, 10 mines)'
        MEDIUM = 'Medium\n(16 x 16, 40 mines)'
        HARD = 'Hard\n(16 x 30, 99 mines)'
        CUSTOM = 'Custom\n(Set manually)'
    
    triggered = Signal(Mode)
    
    def __init__(self, mode: Mode) -> None:
        super().__init__(mode.value)
        if mode == self.Mode.CUSTOM:
            self.setCheckable(True)
        self._mode = mode
        self.clicked.connect(self.on_clicked)
    
    @property
    def mode(self) -> Mode:
        return self._mode
    
    @Slot()
    def on_clicked(self) -> None:
        self.triggered.emit(self.mode)
