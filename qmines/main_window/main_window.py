import json
from importlib import resources as ir

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QSpacerItem, QApplication

from qmines.board.board import Board
from qmines.board.board_tile import Tile, MineCountChange
from qmines.control_elements.mine_counter import MineCounter
from qmines.control_elements.pause_button import PauseButton
from qmines.control_elements.time_tracker import TimeTracker
from qmines.game_parameters import GameParameters, DEFAULT_PARAMS
from qmines.main_window.game_over_types import GameOver


class MainWindow(QMainWindow):

    game_over = Signal(GameOver)
    game_start = Signal(int, int) # Params are coords of first clicked tile.
    
    def __init__(self) -> None:
        super().__init__()
        self._parameters: GameParameters | None = None
        self._game_board: Board | None = None
        self._mine_counter: MineCounter | None = None
        self._time_tracker: TimeTracker | None = None
        self._pause_button: PauseButton | None = None
        self.set_up()
    
    def set_up(self, parameters: GameParameters | None = None) -> None:
        # Menubar still needed
        if parameters is None:
            parameters = self._get_initial_parameters()
        self._parameters = parameters

        window_frame = QFrame()
        self._mine_counter = self._mine_counter_factory()
        self._pause_button = self._pause_button_factory()
        self._time_tracker = self._time_tracker_factory()
        self._game_board = self._board_factory()

        window_layout = QVBoxLayout()
        window_frame.setLayout(window_layout)
        window_layout.addLayout(self._control_layout_factory())
        window_layout.addWidget(self._game_board)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setCentralWidget(window_frame)
        self.show()

    @Slot(int, int)
    def on_mine_exploded(self, i: int, j: int):
        self.game_over.emit(GameOver.MINE_EXPLODED)

    @Slot(int, int)
    def on_first_click(self, i: int, j: int):
        self.game_start.emit(i, j)

    @Slot(int, int)
    def on_revealed_tile_clicked(self, i: int, j: int):
        """
        Reveal all hidden tiles around (i, j) unless it has a flag.
        """
        ...

    @Slot(MineCountChange)
    def on_mine_count_change(self, change: MineCountChange):
        """
        Increase or decrease the mine count in the mine counter.
        """

    @Slot(int, int)
    def on_tile_revealed(self, i: int, j: int):
        """
        If the tile has proximity 0, reveal all neighbours
        """
        ...

    @Slot(GameOver)
    def on_game_over(self, reason: GameOver):
        """
        Emission of the game over signal has already happened
        """
        ...

    @Slot(bool)
    def on_pause(self, paused: bool):
        """
        Tell the tile board to hide itself.
        """
        ...


    @staticmethod
    def _get_initial_parameters() -> GameParameters:
        try:
            param_file = ir.files('qmines') / 'resources' / 'game_params.json'
            param_text = param_file.read_text()
            params_dict = json.loads(param_text)
            return GameParameters(**params_dict)
        except Exception as e:
            print(f'Using default parameters. Saved parameters could not be loaded: {e}')
            return GameParameters(**DEFAULT_PARAMS)

    def _tile_factory(self, index: int) -> Tile:
        tile = Tile(self._parameters.to_coordinates(index))
        tile.mine_exploded.connect(self.on_mine_exploded)
        tile.first_clicked.connect(self.on_first_click)
        tile.revealed_tile_clicked.connect(self.on_revealed_tile_clicked)
        tile.mine_count_change.connect(self.on_mine_count_change)
        tile.tile_revealed.connect(self.on_tile_revealed)
        self.game_over.connect(tile.on_game_over)
        self.game_start.connect(tile.on_game_start)
        return tile

    @staticmethod
    def _mine_counter_factory() -> MineCounter:
        return MineCounter()

    @staticmethod
    def _pause_button_factory() -> PauseButton:
        return PauseButton()

    @staticmethod
    def _time_tracker_factory() -> TimeTracker:
        return TimeTracker()

    def _board_factory(self) -> Board:
        tiles = [self._tile_factory(i) for i in range(self._parameters.size)]
        return Board(self._parameters, tiles)

    def _control_layout_factory(self) -> QHBoxLayout:
        control_layout = QHBoxLayout()
        control_layout.addWidget(self._mine_counter)
        control_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.MinimumExpanding))
        control_layout.addWidget(self._pause_button)
        control_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.MinimumExpanding))
        control_layout.addWidget(self._time_tracker)
        return control_layout

if __name__ == '__main__':
    app = QApplication([])
    mw = MainWindow()
    app.exec()


