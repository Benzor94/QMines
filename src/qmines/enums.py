from enum import Enum


class GameOverReason(Enum):
    WIN = 0
    LOSS = 1


class FlagCountChange(Enum):
    ADDED = 1
    REMOVED = -1

