from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QFrame, QApplication


class MainWindow(QMainWindow):

    def __init__(self, /):
        super().__init__()

        self.button = QPushButton()
        #self.button.setDisabled(True)
        self.button.setCheckable(True)

        self.button_controller_button = QPushButton()
        self.button_controller_button.setCheckable(False)
        self.button_controller_button.setText("Click me!")

        self.btn_layout = QVBoxLayout()
        self.btn_layout.addWidget(self.button)
        self.btn_layout.addWidget(self.button_controller_button)

        self.frame = QFrame()
        self.frame.setLayout(self.btn_layout)

        self.setCentralWidget(self.frame)

        self.button.toggled.connect(self.on_button_check)
        self.button_controller_button.clicked.connect(self.on_button_click)

        self.show()

    def on_button_click(self):
        if not self.button.isChecked():
            self.button.setChecked(True)
        else:
            self.button.setChecked(False)

    def on_button_check(self, checked: bool):
        if checked:
            print("The button has been checked!")

if __name__ == '__main__':
    app = QApplication([])
    mw = MainWindow()
    app.exec()
