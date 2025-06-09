from typing import override

import PySide6.QtWidgets as QW
import PySide6.QtCore as QC
import PySide6.QtGui as QG

from qmines.utilities import set_font_size_based_on_height
from qmines.constants import CONTROL_PANEL_MIN_HEIGHT, CONTROL_PANEL_MAX_HEIGHT

class NewGameButton(QW.QPushButton):

    WIDTH_TO_HEIGHT_RATIO = 2
    
    def __init__(self) -> None:
        super().__init__()
        self.setSizePolicy(QW.QSizePolicy.Policy.Minimum, QW.QSizePolicy.Policy.Minimum)
        set_font_size_based_on_height(self, CONTROL_PANEL_MIN_HEIGHT)
        self.setText('New')
        self.setMaximumHeight(CONTROL_PANEL_MAX_HEIGHT)

    @override
    def sizeHint(self) -> QC.QSize:
        return QC.QSize(round(CONTROL_PANEL_MIN_HEIGHT * self.__class__.WIDTH_TO_HEIGHT_RATIO), CONTROL_PANEL_MIN_HEIGHT)

    @override
    def resizeEvent(self, event: QG.QResizeEvent) -> None:
        new_height = event.size().height()
        new_width = event.size().width()
        set_font_size_based_on_height(self, new_height)
        self.resize(round(new_height * self.__class__.WIDTH_TO_HEIGHT_RATIO), new_height)