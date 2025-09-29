from PySide6.QtWidgets import QApplication

from qmines.application import Application


def main() -> None:
    app = QApplication([])
    _ = Application()
    app.exec()
