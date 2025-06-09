

from typing import Final


class GameParameters:
    MIN_SIZE: Final[int] = 4
    MAX_SIZE: Final[int] = 30
    SIZE_RANGE: Final[range] = range(MIN_SIZE, MAX_SIZE + 1)

    def __init__(self, n_rows: int, n_cols: int, n_mines: int, timeout_in_seconds: int) -> None:
        self._n_rows  = n_rows
        self._n_cols = n_cols
        self._n_mines = n_mines
        self._timeout_in_seconds = int(timeout_in_seconds)

        self._verify_length(n_rows)
        self._verify_length(n_cols)
        self._verify_mine_number()
        self._verify_timeout()
    
    @property
    def n_rows(self) -> int:
        return self._n_rows
    @property
    def n_cols(self) -> int:
        return self._n_cols
    @property
    def number_of_elements(self) -> int:
        return self.n_rows * self.n_cols
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
            raise ValueError(f'Length {length} must be in range [{cls.MIN_SIZE}, {cls.MAX_SIZE}].')
    
    def _verify_mine_number(self) -> None:
        if not 1 <= self._n_mines < self.number_of_elements:
            raise ValueError(f'The number {self._n_mines} of mines must be in range [{1}, {self.number_of_elements - 1}].')
    
    def _verify_timeout(self) -> None:
        if not 0 <= self._timeout_in_seconds:
            raise ValueError(f'Timeout {self._timeout_in_seconds} must be non-negative.')