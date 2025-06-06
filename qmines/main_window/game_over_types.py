from enum import Enum


class GameOver(Enum):
    WIN = 0
    MINE_EXPLODED = 1
    TIME_RAN_OUT = 2