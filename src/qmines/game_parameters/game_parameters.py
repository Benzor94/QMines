from collections.abc import Mapping
from typing import Final

from qmines.utilities.constants import BOARD_MIN_SIZE, BOARD_MAX_SIZE, DEFAULT_SETTINGS


class GameParameters:
    SIZE_RANGE: Final[range] = range(BOARD_MIN_SIZE, BOARD_MAX_SIZE + 1)

    def __init__(self, n_rows: int, n_cols: int, n_mines: int, time_limit_in_seconds: int) -> None:
        self._n_rows  = n_rows
        self._n_cols = n_cols
        self._n_mines = n_mines
        self._time_limit_in_seconds = int(time_limit_in_seconds)

        self._verify_length(n_rows)
        self._verify_length(n_cols)
        self._verify_mine_number()
        self._verify_time_limit()
    
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
    def time_limit_in_seconds(self) -> int:
        return self._time_limit_in_seconds
    @property
    def is_hardcore_mode(self) -> bool:
        return self.time_limit_in_seconds > 0

    @classmethod
    def from_dict(cls, dict_: Mapping[str, int], *,
                  n_rows: int | None = None,
                  n_cols: int | None = None,
                  n_mines: int | None = None,
                  time_limit: int | None = None) -> 'GameParameters':
        n_rows_ = n_rows if n_rows is not None else dict_.get('n_rows', DEFAULT_SETTINGS['n_rows'])
        n_cols_ = n_cols if n_cols is not None else dict_.get('n_cols', DEFAULT_SETTINGS['n_cols'])
        n_mines_ = n_mines if n_mines is not None else dict_.get('n_mines', DEFAULT_SETTINGS['n_mines'])
        time_limit_ = (time_limit if time_limit is not None
                       else dict_.get('time_limit_in_seconds', DEFAULT_SETTINGS['time_limit_in_seconds']))
        return cls(n_rows_, n_cols_, n_mines_, time_limit_)

    @classmethod
    def copy_from(cls, parameters: 'GameParameters', *,
                  n_rows: int | None = None,
                  n_cols: int | None = None,
                  n_mines: int | None = None,
                  time_limit: int | None = None):
        return GameParameters.from_dict(parameters.to_dict(), n_rows=n_rows, n_cols=n_cols, n_mines=n_mines,
                                        time_limit=time_limit)

    def to_dict(self) -> dict[str, int]:
        return {'n_rows': self.n_rows, 'n_cols': self.n_cols, 'n_mines': self.n_mines,
                'time_limit_in_seconds': self.time_limit_in_seconds}
    
    @classmethod
    def _verify_length(cls, length: int) -> None:
        if length not in cls.SIZE_RANGE:
            raise ValueError(f'Length {length} must be in range [{BOARD_MIN_SIZE}, {BOARD_MAX_SIZE}].')
    
    def _verify_mine_number(self) -> None:
        if not 1 <= self._n_mines < self.number_of_elements:
            raise ValueError(f'The number {self._n_mines} of mines must be in range [{1}, {self.number_of_elements - 1}].')
    
    def _verify_time_limit(self) -> None:
        if not 0 <= self._time_limit_in_seconds:
            raise ValueError(f'Timeout {self._time_limit_in_seconds} must be non-negative.')