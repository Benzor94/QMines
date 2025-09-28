from PySide6.QtWidgets import QFrame, QMainWindow, QSizePolicy, QStackedLayout, QToolBar, QWidget


class MainWindow(QMainWindow):

    def __init__(self, board_view: QWidget, pause_view: QWidget, toolbar_view: QToolBar) -> None:
        super().__init__()
        self._board_view = board_view
        self._pause_view = pause_view
        self._toolbar = toolbar_view
        self._layout = QStackedLayout()
        self.setWindowTitle('QMines')
        self._set_size_properties()
        self._set_layout_properties()
        self._set_minimum_size()
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
        frame = QFrame()
        frame.setLayout(self._layout)
        self._layout.addWidget(self._board_view)
        self._layout.addWidget(self._pause_view)
        self.setCentralWidget(frame)
    
    def _set_minimum_size(self) -> None:
        self.adjustSize()
        toolbar_width = self._toolbar.sizeHint().width()
        frame_margin = self.geometry().width() - self.contentsRect().width()
        self.setMinimumWidth(toolbar_width + frame_margin)
    

