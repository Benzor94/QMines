from abc import abstractmethod
from collections.abc import Iterator
from typing import Protocol

from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import QWidget


def range_as_cls_interval(ran: range) -> str:
    return f'[{ran.start}, {ran.stop - 1}]'

def set_font_size_based_on_height(widget: QWidget | QAction, height: int) -> None:
    new_size = height // 2
    current_font = widget.font()
    if current_font.pointSize() != new_size:
        widget.setFont(QFont(current_font.family(), new_size))

class RectangularGrid[T](Protocol):
    
    @property
    @abstractmethod
    def n_rows(self) -> int: ...

    @property
    @abstractmethod
    def n_cols(self) -> int: ...

    @abstractmethod
    def __getitem__(self, coordinates: tuple[int, int]) -> T: ...

def wrap_index(idx: int, length: int) -> int:
    if idx not in (ran := _get_valid_index_range(length)):
        raise ValueError(f'Index {idx} must be in range {range_as_cls_interval(ran)}')
    if idx < 0:
        return length + idx
    return idx

def wrap_coordinates(row: int, col: int, n_rows: int, n_cols: int) -> tuple[int, int]:
    return wrap_index(row, n_rows), wrap_index(col, n_cols)

def convert_index_to_coordinates(idx: int, n_rows: int, n_cols: int) -> tuple[int, int]:
    idx = wrap_index(idx, n_rows * n_cols)
    return idx // n_cols, idx % n_cols

def convert_coordinates_to_index(row: int, col: int, n_rows: int, n_cols: int) -> int:
    row, col = wrap_coordinates(row, col, n_rows, n_cols)
    return row * n_cols + col

def proximity_iterator[T](grid: RectangularGrid[T], row: int, col: int) -> Iterator[T]:
    row, col = wrap_coordinates(row, col, grid.n_rows, grid.n_cols)
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            r = row + i
            c = col + j
            if (0 <= r < grid.n_rows) and (0 <= c < grid.n_cols) and not (i == 0 and j == 0):
                yield grid[r, c]

def _length_is_non_negative(length: int) -> None:
    if length < 0:
        raise ValueError('Length cannot be negative')

def _get_valid_index_range(length: int) -> range:
    _length_is_non_negative(length)
    return range(-length, length)