from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button = QPushButton()
        self.button.setCheckable(False)
        self.button.setText('Click me')

        self.button.clicked.connect(self.on_button_click)

        self.setCentralWidget(self.button)
        self.show()

    @Slot()
    def on_button_click(self) -> None:
        print('Button has been clicked')
        if not self.button.isDown(): self.button.setDown(True)


if __name__ == '__main__':
    app = QApplication([])
    mw = MainWindow()
    app.exec()