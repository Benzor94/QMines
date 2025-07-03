from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import ClassVar

from qmines.constants import BOARD_MAX_LENGTH, BOARD_MIN_LENGTH, EASY_SETTINGS, MINIMUM_TIME_LIMIT, MAXIMUM_TIME_LIMIT
from qmines.utilities import range_as_cls_interval


@dataclass(slots=True, frozen=True)
class Settings:
    LENGTH_RANGE: ClassVar[range] = range(BOARD_MIN_LENGTH, BOARD_MAX_LENGTH + 1)
    n_rows: int
    n_cols: int
    n_mines: int
    time_limit: int

    @classmethod
    def from_dict(
        cls,
        dict_: Mapping[str, int],
        *,
        n_rows: int | None = None,
        n_cols: int | None = None,
        n_mines: int | None = None,
        time_limit: int | None = None,
    ) -> 'Settings':
        n_rows_ = n_rows if n_rows is not None else dict_.get('n_rows', EASY_SETTINGS['n_rows'])
        n_cols_ = n_cols if n_cols is not None else dict_.get('n_cols', EASY_SETTINGS['n_cols'])
        n_mines_ = n_mines if n_mines is not None else dict_.get('n_mines', EASY_SETTINGS['n_mines'])
        time_limit_ = time_limit if time_limit is not None else dict_.get('time_limit', EASY_SETTINGS['time_limit'])

        cls._verify_length(n_rows_)
        cls._verify_length(n_cols_)
        cls._verify_mine_number(n_mines_, n_rows_ * n_cols_)
        cls._verify_time_limit(time_limit_)
        return cls(n_rows=n_rows_, n_cols=n_cols_, n_mines=n_mines_, time_limit=time_limit_)

    def to_dict(self) -> dict[str, int]:
        return asdict(self)

    @classmethod
    def _verify_length(cls, length: int) -> None:
        if length not in cls.LENGTH_RANGE:
            raise ValueError(f'Board length (specified as {length}) must be in {range_as_cls_interval(cls.LENGTH_RANGE)}.')

    @staticmethod
    def _verify_mine_number(n_mines: int, size: int) -> None:
        if not 0 < n_mines < size:
            raise ValueError(f'Mine number (specified as {n_mines}) must be in {range_as_cls_interval(range(1, size))}.')

    @staticmethod
    def _verify_time_limit(time_limit: int) -> None:
        if MINIMUM_TIME_LIMIT <= time_limit <= MAXIMUM_TIME_LIMIT:
            raise ValueError(f'Time limit (specified as {time_limit}) must be non-negative.')
