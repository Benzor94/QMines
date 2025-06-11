import PySide6.QtWidgets as QW

from qmines.board.board import Board
from qmines.board.tile import Tile
from qmines.control_panel.control_panel import ControlPanel
from qmines.game_parameters.game_parameters import GameParameters
from qmines.game_parameters.settings_reader import read_settings


class MainWindow(QW.QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self._parameters: GameParameters
        self._board: Board
        self._control_panel: ControlPanel
        self._frame: QW.QFrame
        self._frame_layout: QW.QVBoxLayout
        self.set_up()
    
    def set_up(self, parameters: GameParameters | None = None) -> None:
        if parameters is None:
            parameters = read_settings()
        self._parameters = parameters
        self._set_toolbar()
        self._frame = QW.QFrame()
        self._board = self._board_factory()

        self._frame_layout = QW.QVBoxLayout()
        self._frame_layout.addWidget(self._board)
        self._frame.setLayout(self._frame_layout)

        self.setSizePolicy(QW.QSizePolicy.Policy.Minimum, QW.QSizePolicy.Policy.Minimum)
        self.setCentralWidget(self._frame)
        self.show()
    
    def _board_factory(self) -> Board:
        """Temporary"""
        assert self._parameters is not None
        tiles = [Tile((idx // self._parameters.n_cols, idx % self._parameters.n_cols)) for idx in range(self._parameters.number_of_elements)]
        return Board(parameters=self._parameters, tiles=tiles)

    def _set_toolbar(self) -> None:
        self._control_panel = ControlPanel()
        self.addToolBar(self._control_panel)
    