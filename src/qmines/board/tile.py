from typing import Final, override
import PySide6.QtWidgets as QW
import PySide6.QtCore as QC
import PySide6.QtGui as QG

from qmines.utilities import set_font_size_based_on_height

class Tile(QW.QPushButton):
    MIN_SIZE: Final[int] = 25

    def __init__(self, coordinates: tuple[int, int] = (0, 0)) -> None:
        super().__init__()
        self._coordinates = coordinates

        self.setSizePolicy(QW.QSizePolicy.Policy.Minimum, QW.QSizePolicy.Policy.Minimum)
        set_font_size_based_on_height(self, self.size().height())
    
    @property
    def coordinates(self) -> tuple[int, int]:
        return self._coordinates
    
    @override
    def sizeHint(self) -> QC.QSize:
        return QC.QSize(self.__class__.MIN_SIZE, self.__class__.MIN_SIZE)
    
    @override
    def resizeEvent(self, event: QG.QResizeEvent) -> None:
        new_height = event.size().height()
        set_font_size_based_on_height(self, new_height)