

from abc import abstractmethod
from collections.abc import Iterable, Iterator
from typing import Protocol


class AbstractGrid[T](Iterable[T], Protocol):
    """
    Generic abstract class representing a finite rectangular grid of elements of type T.
    """
    @property
    @abstractmethod
    def n_rows(self) -> int: ...

    @property
    @abstractmethod
    def n_cols(self) -> int: ...

    @abstractmethod
    def __getitem__(self, coordinates: tuple[int, int]) -> T: ...

    @property
    def number_of_elements(self) -> int:
        return self.n_rows * self.n_cols
    
    def wrap_index(self, idx: int) -> int:
        if idx not in self._valid_index_range:
            raise IndexError(f'Index {idx} must be in range [{-self.number_of_elements}, {self.number_of_elements - 1}].')
        if idx < 0:
            return self.number_of_elements + idx
        return idx
    
    def wrap_coordinates(self, i: int, j: int) -> tuple[int, int]:
        if (i not in self._valid_row_range) or (j not in self._valid_column_range):
            raise IndexError(f'Coordinates {i} and {j} must be in [{-self.n_rows}, {self.n_rows - 1}] and [{-self.n_cols}, {self.n_cols - 1}], respectively.')
        wrapped_i, wrapped_j = i, j
        if wrapped_i < 0:
            wrapped_i = self.n_rows + wrapped_i
        if wrapped_j < 0:
            wrapped_j = self.n_cols + wrapped_j
        return wrapped_i, wrapped_j
    
    def to_coordinates(self, idx: int) -> tuple[int, int]:
        idx = self.wrap_index(idx)
        return idx // self.n_cols, idx % self.n_cols
    
    def to_index(self, i: int, j: int) -> int:
        i, j = self.wrap_coordinates(i, j)
        return i * self.n_cols + j
    
    def proximity_iterator(self, i: int, j: int) -> Iterator[T]:
        for p in (-1, 0, 1):
            for q in (-1, 0, 1):
                row, col = i + p, j + q
                if self._coordinates_are_on_grid(row, col) and not (p == 0 and q == 0):
                    yield self[row, col]
    
    def _coordinates_are_on_grid(self, i: int, j: int) -> bool:
        return (0 <= i < self.n_rows) and (0 <= j < self.n_cols)
    
    @property
    def _valid_index_range(self) -> range:
        return range(-self.number_of_elements, self.number_of_elements)
    
    @property
    def _valid_row_range(self) -> range:
        return range(-self.n_rows, self.n_rows)
    
    @property
    def _valid_column_range(self) -> range:
        return range(-self.n_cols, self.n_cols)
    