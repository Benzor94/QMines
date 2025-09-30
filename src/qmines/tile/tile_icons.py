from pathlib import Path
from typing import Final

from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon

from qmines.utilities import get_resources_dir


class TileIconRepository(QObject):
    
    MINE_ICON: Final[Path] = get_resources_dir() / 'mine256.png'
    FLAG_ICON: Final[Path] = get_resources_dir() / 'flag256.png'
    BOOM_ICON: Final[Path] = get_resources_dir() / 'explosion256.png'

    def __init__(self) -> None:
        self._empty_icon = QIcon()
        self._mine_icon = QIcon(str(self.MINE_ICON.resolve()))
        self._flag_icon = QIcon(str(self.FLAG_ICON.resolve()))
        self._boom_icon = QIcon(str(self.BOOM_ICON.resolve()))
    
    @property
    def empty(self) -> QIcon:
        return self._empty_icon
    
    @property
    def mine(self) -> QIcon:
        return self._mine_icon
    
    @property
    def flag(self) -> QIcon:
        return self._flag_icon
    
    @property
    def explosion(self) -> QIcon:
        return self._boom_icon