from enum import Enum

import PySide6.QtWidgets as QW
from PySide6.QtCore import Slot, Signal

from qmines.board.board import Board
from qmines.board.tile import Tile
from qmines.utilities.constants import DEFAULT_SETTINGS
from qmines.control_panel.control_panel import ControlPanel
from qmines.game_parameters.game_parameters import GameParameters
from qmines.game_parameters.settings_reader import write_settings
from qmines.utilities.index_tools import convert_index_to_coordinates
from qmines.global_state import StateTracker

class GameOver(Enum):
    WIN = 0
    MINE_EXPLODED = 1
    TIME_RAN_OUT = 2

class MainWindow(QW.QMainWindow):

    game_over = Signal(GameOver)
    game_start = Signal(int, int)

    def __init__(self, parameters: GameParameters | None) -> None:
        super().__init__()
        self._parameters = parameters
        self._board: Board
        self._control_panel: ControlPanel
        self._frame: QW.QFrame
        self._frame_layout: QW.QVBoxLayout
        self._unrevealed_tiles: int
        self.set_up(parameters)
    
    def set_up(self, parameters: GameParameters | None = None) -> None:
        if parameters is None:
            parameters = GameParameters.from_dict(DEFAULT_SETTINGS)
        self._remove_toolbars()
        self._parameters = parameters
        self._unrevealed_tiles = self._parameters.number_of_elements
        self._set_toolbar()
        self._frame = QW.QFrame()
        self._set_board()

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

    @Slot(int, int)
    def on_first_click(self, i: int, j: int) -> None:
        self._set_up_mines(i, j)
        StateTracker.game_is_active = True
        self.game_start.emit(i, j)

    @Slot(int, int, bool)
    def on_tile_revealed(self, i: int, j: int, is_mine: bool) -> None:
        print(f'Tile ({i}, {j}) has been revealed. Is mine: {is_mine}')

    @Slot(int, int)
    def on_revealed_tile_clicked(self, i: int, j: int) -> None:
        ...

    def _set_board(self) -> None:
        tiles = [self._tile_factory(idx) for idx in range(self._parameters.number_of_elements)]
        self._board = Board(parameters=self._parameters, tiles=tiles)

    def _set_toolbar(self) -> None:
        self._control_panel = ControlPanel(self._parameters)
        self.addToolBar(self._control_panel)
        self._control_panel.new_game_dialog.start_new_game.connect(self.on_new_game)
        self._control_panel.pause_state_change.connect(self.on_pause)
        self.game_over.connect(self._control_panel.on_game_over)

    def _remove_toolbars(self) -> None:
        for tb in self.findChildren(QW.QToolBar):
            self.removeToolBar(tb)

    def _tile_factory(self, idx: int) -> Tile:
        tile = Tile(convert_index_to_coordinates(idx, self._parameters.n_rows, self._parameters.n_cols))
        tile.first_click_in_game.connect(self.on_first_click)
        tile.tile_revealed.connect(self.on_tile_revealed)
        tile.revealed_tile_clicked.connect(self.on_revealed_tile_clicked)
        self.game_start.connect(tile.on_game_start)
        return tile

    def _set_up_mines(self, clicked_row: int, clicked_column: int) -> None:
        ...

    