from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication

from qmines.game_parameters import GameParameters
from qmines.main_window.main_window import MainWindow


class ApplicationContext(QObject):

    def __init__(self):
        super().__init__()
        self.application: QApplication | None = None
        self.main_window: MainWindow | None = None
        self.unrevealed_tiles: int | None = None
