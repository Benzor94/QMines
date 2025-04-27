

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

"""
To see how to replace the main window with another.
"""


class AppController:

    def __init__(self) -> None:
        self.mainwindow = QMainWindow()

        self.button = QPushButton()
        self.button.setCheckable(True)
        self.button.setText("Click me!")

        self.button.clicked.connect(self.on_click)

        self.mainwindow.setCentralWidget(self.button)
        self.mainwindow.show()
    
    def replace_main_window(self) -> None:

        self.mainwindow.hide()

        new_main_window = QMainWindow()
        label = QLabel()
        label.setText("No more clicky")

        new_main_window.setCentralWidget(label)
        new_main_window.show()
        self.mainwindow = new_main_window
    
    def on_click(self) -> None:
        self.replace_main_window()


if __name__ == '__main__':
    app = QApplication([])
    ctrl = AppController()

    app.exec()