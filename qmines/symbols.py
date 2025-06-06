
from enum import Enum


class Symbols(Enum):
    MINE = '\U0001F4A3'
    FLAG = '\U0001F6A9'
    PAUSE = '\u23F8'
    PLAY = '\u25B6'
    EXPLOSION = '\U0001F4A5'

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

INDEX_MAP = {0: '', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
             -1: Symbols.FLAG.value, -2: Symbols.MINE.value, -3: Symbols.EXPLOSION.value}
