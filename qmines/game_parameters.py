from types import MappingProxyType
from typing import Final

DEFAULT_PARAMS = MappingProxyType({'n_rows': 8,
                                   'n_cols': 8,
                                   'n_mines': 10,
                                   'timeout_in_seconds': 0})


class GameParameters:
    MIN_SIZE: Final[int] = 4
    MAX_SIZE: Final[int] = 30
    SIZE_RANGE: Final[range] = range(MIN_SIZE, MAX_SIZE + 1)

    def __init__(self, n_rows: int, n_cols: int, n_mines: int, timeout_in_seconds: int) -> None:
        self._verify_length(n_rows)
        self._verify_length(n_cols)
        self._n_rows = n_rows
        self._n_cols = n_cols

        self._verify_mine_number(n_mines)
        self._n_mines = n_mines

        self._verify_timeout(timeout_in_seconds)
        self._timeout_in_seconds = int(timeout_in_seconds)

        self._idx_valid_range = range(-self.size, self.size)
        self._row_valid_range = range(-self.n_rows, self.n_rows)
        self._col_valid_range = range(-self.n_cols, self.n_cols)
    
    @property
    def n_rows(self) -> int:
        return self._n_rows
    @property
    def n_cols(self) -> int:
        return self._n_cols
    @property
    def size(self) -> int:
        return self.n_rows * self._n_cols
    @property
    def n_mines(self) -> int:
        return self._n_mines
    @property
    def timeout_in_seconds(self) -> int:
        return self._timeout_in_seconds
    @property
    def is_hardcore_mode(self) -> bool:
        return self.timeout_in_seconds > 0
    
    @classmethod
    def _verify_length(cls, length: int) -> None:
        if length not in cls.SIZE_RANGE:
            raise ValueError(f'Length {length} must be in size range [{cls.MIN_SIZE}, {cls.MAX_SIZE}].')
    
    def _verify_mine_number(self, n_mines: int) -> None:
        if not 1 <= n_mines <= self.size - 1:
            raise ValueError(f'The number of mines {n_mines} must be in range [{1}, {self.size - 1}].')

    def _verify_timeout(self, timeout: int) -> None:
        if not 0 <= timeout:
            raise ValueError(f'Timeout {timeout} must be non-negative.')
    
    def wrap_index(self, idx: int) -> int:
        if idx not in self._idx_valid_range:
            raise IndexError(f'Index {idx} must be in range [{-self.size}, {self.size - 1}].')
        if idx < 0:
            return self.size + idx
        return idx
    
    def wrap_coordinates(self, i: int, j: int) -> tuple[int, int]:
        if (i not in self._row_valid_range) or (j not in self._col_valid_range):
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
    
