from PySide6.QtWidgets import QFrame, QMainWindow, QSizePolicy, QToolBar, QVBoxLayout

from qmines.state.state_manager import StateManager
from qmines.status_bar.status_bar import StatusBar
from qmines.toolbar import Toolbar


class MainWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self._state_manager = StateManager()
        self._config = self._state_manager.config

        self._remove_toolbars()
        self._toolbar = self._create_toolbar()
        self._status_bar = self._create_status_bar()
        self._frame = QFrame()
        self._board = self._create_board()
        self._set_layout()
        self._set_size_properties()
        self.setCentralWidget(self._frame)
        self.show()
    
    def _remove_toolbars(self) -> None:
        for tb in self.findChildren(QToolBar):
            self.removeToolBar(tb)
    
    def _create_toolbar(self) -> Toolbar:
        toolbar = Toolbar()
        self.addToolBar(toolbar)
        return toolbar
    
    def _create_status_bar(self) -> StatusBar:
        status_bar = StatusBar()
        self.setStatusBar(status_bar)
        return status_bar
    
    def _create_board(self) -> None:
        ...
    
    def _set_layout(self) -> None:
        frame_layout = QVBoxLayout()
        #frame_layout.addWidget(self._board)
        self._frame.setLayout(frame_layout)
    
    def _set_size_properties(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)