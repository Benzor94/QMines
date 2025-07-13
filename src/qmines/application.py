from collections.abc import Sequence

from PySide6.QtWidgets import QApplication

from qmines.main_window import MainWindow


class Application(QApplication):

    def __init__(self, arguments: Sequence[str]) -> None:
        super().__init__(arguments)

        self._main_window: MainWindow | None = None
    
    def create_main_window(self) -> None:
        self._main_window = MainWindow()
    
    def replace_main_window(self) -> None:
        if self._main_window is None:
            self.create_main_window()
            return
        old_mw = self._main_window
        self._main_window = None
        old_mw.destroy()
        self.create_main_window()