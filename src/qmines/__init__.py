import PySide6.QtWidgets as qw

from qmines.game_parameters.settings_reader import read_settings
from qmines.main_window import MainWindow

def main() -> None:
    
    app = qw.QApplication()
    parameters = read_settings()
    mw = MainWindow(parameters)  # noqa: F841 # pyright: ignore [reportUnusedVariable]
    app.exec()
