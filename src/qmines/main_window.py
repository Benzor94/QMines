import PySide6.QtWidgets as QW
from PySide6.QtCore import Slot

from qmines.board.board import Board
from qmines.board.tile import Tile
from qmines.constants import DEFAULT_SETTINGS
from qmines.control_panel.control_panel import ControlPanel
from qmines.game_parameters.game_parameters import GameParameters
from qmines.game_parameters.settings_reader import write_settings


class MainWindow(QW.QMainWindow):

    def __init__(self, parameters: GameParameters | None) -> None:
        super().__init__()
        self._parameters = parameters
        self._board: Board
        self._control_panel: ControlPanel
        self._frame: QW.QFrame
        self._frame_layout: QW.QVBoxLayout
        self.set_up(parameters)
    
    def set_up(self, parameters: GameParameters | None = None) -> None:
        if parameters is None:
            parameters = GameParameters.from_dict(DEFAULT_SETTINGS)
        self._remove_toolbars()
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

    @Slot(GameParameters)
    def on_new_game(self, parameters: GameParameters) -> None:
        self.set_up(parameters)
        self.adjustSize()
        write_settings(parameters)

    @Slot(bool)
    def on_pause(self, paused: bool) -> None:
        if paused:
            self._board.hide()
        else:
            self._board.show()

    def _board_factory(self) -> Board:
        """Temporary"""
        assert self._parameters is not None
        tiles = [Tile((idx // self._parameters.n_cols, idx % self._parameters.n_cols)) for idx in range(self._parameters.number_of_elements)]
        return Board(parameters=self._parameters, tiles=tiles)

    def _set_toolbar(self) -> None:
        self._control_panel = ControlPanel(self._parameters)
        self.addToolBar(self._control_panel)
        self._control_panel.new_game_dialog.start_new_game.connect(self.on_new_game)
        self._control_panel.pause_state_change.connect(self.on_pause)

    def _remove_toolbars(self) -> None:
        for tb in self.findChildren(QW.QToolBar):
            self.removeToolBar(tb)

    