from PySide6.QtWidgets import QLabel, QStatusBar


class StatusBar(QStatusBar):

    def __init__(self):
        super().__init__()
        self._status_label = QLabel('Hi, this is da game')
        self.addWidget(self._status_label)
        # TBD