from typing import Final

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton, QSpinBox

from qmines.config import Config


class CustomModeSelector(QFrame):

    MIN_BOARD_LENGTH: Final[int] = 8
    MAX_BOARD_LENGTH: Final[int] = 30
    MIN_MINE_NUMBER: Final[int] = 10
    MIN_EMPTY_TILE_NUMBER: Final[int] = 10
    PREFERRED_MINE_DENSITY: Final[float] = 0.156

    def __init__(self, initial_config: Config) -> None:
        super().__init__()
        self._initial_config = initial_config
        self._height_selector = QSpinBox()
        self._width_selector = QSpinBox()
        self._mine_selector = QSpinBox()
        self._start_button = QPushButton('Start custom game')
        self._layout = QGridLayout()
        self._set_selector_properties()
        self._set_layout_properties()
        self.setVisible(False)
    
    @property
    def height_selector(self) -> QSpinBox:
        return self._height_selector
    
    @property
    def width_selector(self) -> QSpinBox:
        return self._width_selector
    
    @property
    def mine_selector(self) -> QSpinBox:
        return self._mine_selector
    
    @property
    def start_button(self) -> QPushButton:
        return self._start_button
    
    @property
    def current_config(self) -> Config:
        return Config(self.height_selector.value(), self.width_selector.value(), self.mine_selector.value())
    
    @Slot()
    def on_board_length_value_change(self) -> None:
        self.mine_selector.setMaximum(self._current_max_mines())
        self.mine_selector.setValue(round(self.height_selector.value() * self.width_selector.value() * self.PREFERRED_MINE_DENSITY))
    
    def _set_selector_properties(self) -> None:
        self.height_selector.setMinimum(self.MIN_BOARD_LENGTH)
        self.height_selector.setMaximum(self.MAX_BOARD_LENGTH)
        self.height_selector.setValue(self._initial_config.number_of_rows)
        self.width_selector.setMinimum(self.MIN_BOARD_LENGTH)
        self.width_selector.setMaximum(self.MAX_BOARD_LENGTH)
        self.width_selector.setValue(self._initial_config.number_of_columns)
        self.mine_selector.setMinimum(self.MIN_MINE_NUMBER)
        self.mine_selector.setMaximum(self._current_max_mines())
        
        self.height_selector.valueChanged.connect(self.on_board_length_value_change)
        self.width_selector.valueChanged.connect(self.on_board_length_value_change)
    
    def _set_layout_properties(self) -> None:
        self._layout.addWidget(QLabel('Rows: '), 0, 0)
        self._layout.addWidget(self.height_selector, 0, 1)
        self._layout.addWidget(QLabel('Columns: '), 1, 0)
        self._layout.addWidget(self.width_selector, 1, 1)
        self._layout.addWidget(QLabel('Mines: '), 2, 0)
        self._layout.addWidget(self.mine_selector, 2, 1)
        self._layout.addWidget(self.start_button, 3, 1, 1, 2)
        self.setLayout(self._layout)
    
    def _current_max_mines(self) -> int:
        return self._height_selector.value() * self._width_selector.value() - self.MIN_EMPTY_TILE_NUMBER
    