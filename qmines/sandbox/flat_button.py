from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QFrame, QApplication


class MainWindow(QMainWindow):

    def __init__(self, /):
        super().__init__()

        self.button = QPushButton()
        self.button.setText("A flat button.")
        self.button.setFlat(True)
        self.button.setDisabled(True)

        self.button_controller_button = QPushButton()
        self.button_controller_button.setCheckable(True)
        self.button_controller_button.setText("Click me!")

        self.btn_layout = QVBoxLayout()
        self.btn_layout.addWidget(self.button)
        self.btn_layout.addWidget(self.button_controller_button)

        self.frame = QFrame()
        self.frame.setLayout(self.btn_layout)

        self.setCentralWidget(self.frame)

        self.button_controller_button.toggled.connect(self.on_button_toggle)

        self.show()

    def on_button_toggle(self, checked: bool):
        if checked:
            self.button_controller_button.setText("A checked button.")
        else:
            self.button_controller_button.setText("Click me!")


if __name__ == '__main__':
    app = QApplication([])
    mw = MainWindow()
    app.exec()
