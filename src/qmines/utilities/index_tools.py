from abc import abstractmethod
from collections.abc import Iterator
from typing import Protocol


class RectangularGrid[T](Protocol):

    @property
    @abstractmethod
    def n_rows(self) -> int: ...

    @property
    @abstractmethod
    def n_cols(self) -> int: ...

    @abstractmethod
    def __getitem__(self, coordinates: tuple[int, int]) -> T: ...

def _length_is_non_negative(length: int) -> None:
    if length < 0:
        raise ValueError('Length cannot be negative.')

def _get_valid_index_range(length: int) -> range:
    _length_is_non_negative(length)
    return range(-length, length)

def wrap_index(idx: int, length: int) -> int:
    _length_is_non_negative(length)
    if idx not in _get_valid_index_range(length):
        raise IndexError(f'Index {idx} must be in range [{-length}, {length - 1}].')
    if idx < 0:
        return length + idx
    return idx

def wrap_coordinates(i: int, j: int, n_rows: int, n_cols: int) -> tuple[int, int]:
    return wrap_index(i, n_rows), wrap_index(j, n_cols)

def convert_index_to_coordinates(idx: int, n_rows: int, n_cols: int) -> tuple[int, int]:
    idx = wrap_index(idx, n_rows * n_cols)
    return idx // n_cols, idx % n_cols

def convert_coordinates_to_index(i: int, j: int, n_rows: int, n_cols: int) -> int:
    i, j = wrap_coordinates(i, j, n_rows, n_cols)
    return i * n_cols + j

def proximity_iterator[T](grid: RectangularGrid[T], i: int, j: int) -> Iterator[T]:
    i, j = wrap_coordinates(i, j, grid.n_rows, grid.n_cols)
    for k in (-1, 0, 1):
        for l in (-1, 0, 1):
            row = i + k
            col = j + l
            if (0 <= row < grid.n_rows) and (0 <= col < grid.n_cols) and not (k == 0 and l == 0):
                yield grid[row, col]