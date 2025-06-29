import PySide6.QtWidgets as qw

from qmines.game_parameters.settings_reader import read_settings
from qmines.main_window import MainWindow
from qmines.state_processor import StateProcessor

def main() -> None:
    
    app = qw.QApplication()
    parameters = read_settings()
    state_processor = StateProcessor()
    state_processor.parameters = parameters
    mw = MainWindow()  # noqa: F841 # pyright: ignore [reportUnusedVariable]
    app.exec()
