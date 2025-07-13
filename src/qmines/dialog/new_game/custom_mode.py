from enum import Enum

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QSpinBox

from qmines.constants import BOARD_MAX_LENGTH, BOARD_MIN_LENGTH, PREFERRED_MINE_DENSITY
from qmines.state.state_manager import StateManager


class BoardDimension(Enum):
    HEIGHT = 0
    WIDTH = 1


class CustomModeLengthSpinbox(QSpinBox):
    def __init__(self, dimension: BoardDimension) -> None:
        super().__init__()
        self._config = StateManager().config
        self._dimension = dimension
        self._label = QLabel('Rows: ' if dimension == BoardDimension.HEIGHT else 'Columns: ')
        self.setMinimum(BOARD_MIN_LENGTH)
        self.setMaximum(BOARD_MAX_LENGTH)
        self.setValue(self._config.n_rows if dimension == BoardDimension.HEIGHT else self._config.n_cols)

    @property
    def label(self) -> QLabel:
        return self._label


class CustomModeMineSpinbox(QSpinBox):
    def __init__(self) -> None:
        super().__init__()
        self._config = StateManager().config
        self._label = QLabel('Mines: ')
        self.setMinimum(1)
        self.setMaximum(self._config.n_rows * self._config.n_cols - 1)
        self.setValue(self._config.n_mines)

    @property
    def label(self) -> QLabel:
        return self._label

    def update_upper_limit(self, board_size: int) -> None:
        self.setMaximum(board_size - 1)
        self.setValue(round(board_size * PREFERRED_MINE_DENSITY))


class CustomModeSettingsLayout(QGridLayout):
    def __init__(self) -> None:
        super().__init__()
        self._row_spinbox = CustomModeLengthSpinbox(BoardDimension.HEIGHT)
        self._column_spinbox = CustomModeLengthSpinbox(BoardDimension.WIDTH)
        self._mine_spinbox = CustomModeMineSpinbox()
        self._start_button = QPushButton('Start custom game')
        self.addWidget(self.row_spinbox.label, 0, 0)
        self.addWidget(self.row_spinbox, 0, 1)
        self.addWidget(self.column_spinbox.label, 1, 0)
        self.addWidget(self.column_spinbox, 1, 1)
        self.addWidget(self.mine_spinbox.label, 2, 0)
        self.addWidget(self.mine_spinbox, 2, 1)
        self.addWidget(self.start_button, 3, 1, 1, 2)
        self._set_up_connections()

    @property
    def row_spinbox(self) -> CustomModeLengthSpinbox:
        return self._row_spinbox

    @property
    def column_spinbox(self) -> CustomModeLengthSpinbox:
        return self._column_spinbox

    @property
    def mine_spinbox(self) -> CustomModeMineSpinbox:
        return self._mine_spinbox

    @property
    def start_button(self) -> QPushButton:
        return self._start_button

    @property
    def row_number(self) -> int:
        return self.row_spinbox.value()

    @property
    def column_number(self) -> int:
        return self.column_spinbox.value()

    @property
    def mine_number(self) -> int:
        return self.mine_spinbox.value()

    @Slot(int)
    def on_size_change(self) -> None:
        new_board_size = self.row_number * self.column_number
        self.mine_spinbox.update_upper_limit(new_board_size)

    def _set_up_connections(self) -> None:
        self.row_spinbox.valueChanged.connect(self.on_size_change)
        self.column_spinbox.valueChanged.connect(self.on_size_change)
