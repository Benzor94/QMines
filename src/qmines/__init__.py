import PySide6.QtWidgets as qw

from qmines.main_window import MainWindow

def main() -> None:
    
    app = qw.QApplication()
    mw = MainWindow()  # noqa: F841 # pyright: ignore [reportUnusedVariable]
    app.exec()
