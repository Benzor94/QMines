from collections.abc import Callable
from enum import Enum

from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton, QSpinBox


class BoardLengthSelector(QSpinBox):

    class Dimension(Enum):
        HEIGHT = 0
        WIDTH = 1
    
    def __init__(self, dimension: Dimension, min_length: int, max_length: int, initial_value: int) -> None:
        super().__init__()
        self._dimension = dimension
        self._label = self._create_label()
        self.setMinimum(min_length)
        self.setMaximum(max_length)
        self.setValue(initial_value)
    
    @property
    def label(self) -> QLabel:
        return self._label
 
    def _create_label(self) -> QLabel:
        match self._dimension:
            case self.Dimension.HEIGHT:
                text = 'Rows: '
            case self.Dimension.WIDTH:
                text = 'Columns: '
        return QLabel(text)

class MineCountSelector(QSpinBox):

    def __init__(self, min_count: int, max_count: Callable[[int], int], initial_value: int, initial_board_size: int, preferred_mine_density: float) -> None:
        super().__init__()
        self._label = QLabel('Mines: ')
        self._max_count_fcn = max_count
        self._preferred_mine_density = preferred_mine_density
        self.setMinimum(min_count)
        self.setMaximum(max_count(initial_board_size))
        self.setValue(initial_value)
    
    @property
    def label(self) -> QLabel:
        return self._label
    
    def update_max(self, current_board_size: int) -> None:
        self.setMaximum(self._max_count_fcn(current_board_size))
        self.setValue(round(current_board_size * self._preferred_mine_density))


class CustomModeSelector(QFrame):

    def __init__(self, height_selector: BoardLengthSelector, width_selector: BoardLengthSelector, mine_selector: MineCountSelector, start_button: QPushButton) -> None:
        super().__init__()
        self._height_selector = height_selector
        self._width_selector = width_selector
        self._mine_selector = mine_selector
        self._start_button = start_button
        self._layout = QGridLayout()
        self._set_layout_properties()
        self.setVisible(False)
    
    def _set_layout_properties(self) -> None:
        self._layout.addWidget(self._height_selector.label, 0, 0)
        self._layout.addWidget(self._height_selector, 0, 1)
        self._layout.addWidget(self._width_selector.label, 1, 0)
        self._layout.addWidget(self._width_selector, 1, 1)
        self._layout.addWidget(self._mine_selector.label, 2, 0)
        self._layout.addWidget(self._mine_selector, 2, 1)
        self._layout.addWidget(self._start_button, 3, 1, 1, 2)
        self.setLayout(self._layout)
    