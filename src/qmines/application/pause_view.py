from typing import Final

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel


class PauseView(QLabel):

    FONT_SIZE: Final[int] = 24

    def __init__(self) -> None:
        super().__init__()
        self.setText('Game paused')
        #self.setStyleSheet('border: 2px dashed red')
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._set_font_properties()
    
    def _set_font_properties(self) -> None:
        current_font = self.font()
        current_font.setBold(True)
        self.setFont(QFont(current_font.family(), self.FONT_SIZE))