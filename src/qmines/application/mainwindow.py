from PySide6.QtWidgets import QFrame, QMainWindow, QMenuBar, QSizePolicy, QStackedLayout, QToolBar, QWidget


class MainWindow(QMainWindow):
    def __init__(self, board_view: QWidget, pause_view: QWidget, toolbar_view: QToolBar, menubar: QMenuBar) -> None:
        super().__init__()
        self._board_view = board_view
        self._pause_view = pause_view
        self._toolbar = toolbar_view
        self._menubar = menubar
        self._layout = QStackedLayout()
        self.setWindowTitle('QMines')
        self._set_size_properties()
        self._set_layout_properties()
        self.show()

    def set_paused(self, paused: bool) -> None:
        if paused:
            self._layout.setCurrentWidget(self._pause_view)
        else:
            self._layout.setCurrentWidget(self._board_view)

    def _set_size_properties(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    def _set_layout_properties(self) -> None:
        self.addToolBar(self._toolbar)
        self.setMenuBar(self._menubar)
        frame = QFrame()
        frame.setLayout(self._layout)
        self._layout.addWidget(self._board_view)
        self._layout.addWidget(self._pause_view)
        self.setCentralWidget(frame)

