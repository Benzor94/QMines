
from enum import Enum
from importlib.abc import Traversable
from importlib.resources import files
from types import MappingProxyType
from typing import Final

SETTINGS_FILE: Final[Traversable] = files('qmines') / 'resources' / 'qmines_settings.json'
DEFAULT_SETTINGS: Final[MappingProxyType[str, int]] = MappingProxyType({'n_rows': 8,
                                                                        'n_cols': 8,
                                                                        'n_mines': 10,
                                                                        'timeout_in_seconds': 0})

CONTROL_PANEL_MIN_HEIGHT: Final[int] = 30
CONTROL_PANEL_MAX_HEIGHT: Final[int] = 60

class Symbol(Enum):
    MINE = '\U0001F4A3'
    FLAG = '\U0001F6A9'
    PAUSE = '\u23F8'
    PLAY = '\u25B6'
    EXPLOSION = '\U0001F4A5'
    INFINITY = u"\u221E"

class TileSymbol(Enum):
    EMPTY = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    FLAG = -1
    MINE = -2
    EXPLOSION = -3

INDEX_MAP: Final[MappingProxyType[int, str]] = MappingProxyType({0: '', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
                                                                 -1: Symbol.FLAG.value, -2: Symbol.MINE.value, -3: Symbol.EXPLOSION.value})