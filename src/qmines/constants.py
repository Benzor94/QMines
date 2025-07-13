from enum import Enum
from types import MappingProxyType
from typing import Final

BOARD_MIN_LENGTH: Final[int] = 4
BOARD_MAX_LENGTH: Final[int] = 30

DEFAULT_TIME_LIMIT: Final[int] = 120
MINIMUM_TIME_LIMIT: Final[int] = 10
MAXIMUM_TIME_LIMIT: Final[int] = 3600

PREFERRED_MINE_DENSITY: Final[float] = 0.156

EASY_SETTINGS: Final[MappingProxyType] = MappingProxyType({'n_rows': 8, 'n_cols': 8, 'n_mines': 10, 'time_limit': 0})
MEDIUM_SETTINGS: Final[MappingProxyType] = MappingProxyType({'n_rows': 16, 'n_cols': 16, 'n_mines': 40, 'time_limit': 0})
HARD_SETTINGS: Final[MappingProxyType] = MappingProxyType({'n_rows': 16, 'n_cols': 30, 'n_mines': 99, 'time_limit': 0})


class Symbol(Enum):
    MINE = '\U0001f4a3'
    FLAG = '\U0001f6a9'
    PAUSE = '\u23f8'
    PLAY = '\u25b6'
    EXPLOSION = '\U0001f4a5'
    INFINITY = '\u221e'
    TIMER = '\N{ALARM CLOCK}'
