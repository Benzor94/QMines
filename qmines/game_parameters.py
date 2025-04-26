
from typing import Final, cast


class GameParameters:
    MIN_SIZE: Final[int] = 4
    MAX_SIZE: Final[int] = 100
    SIZE_RANGE: Final[range] = range(MIN_SIZE, MAX_SIZE + 1)

    def __init__(self, n_rows: int, n_cols: int, *, n_mines: int | None = None, density: float | None = None) -> None:
        self._verify_length(n_rows)
        self._verify_length(n_cols)
        self._n_rows = n_rows
        self._n_cols = n_cols

        if n_mines is None and density is None:
            raise ValueError('Either mine number or mine density must be specified.')
        
        if density is not None:
            n_mines = round(self.size * density)
        n_mines = cast(int, n_mines)
        self._verify_mine_number(n_mines)
        self._n_mines = n_mines
    
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
    
    @classmethod
    def _verify_length(cls, length: int) -> None:
        if length not in cls.SIZE_RANGE:
            raise ValueError(f'Length {length} must be in size range [{cls.MIN_SIZE}, {cls.MAX_SIZE}].')
    
    def _verify_mine_number(self, n_mines: int) -> None:
        if not 1 <= n_mines <= self.size - 1:
            raise ValueError(f'The number of mines {n_mines} must be in range [{1}, {self.size - 1}].')