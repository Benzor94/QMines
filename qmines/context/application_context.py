from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication


class ApplicationContext(QObject):

    def __init__(self):
        super().__init__()
        self.application: QApplication | None = None
        self.main_window: ... | None = None