from enum import Enum


class GameOverReason(Enum):
    WIN = 0
    LOSS = 1


class FlagCountChange(Enum):
    ADDED = 1
    REMOVED = -1


class IconState(Enum):
    EMPTY = 0
    FLAG = 1
    MINE = 2
    EXPLOSION = 3


class PressedState(Enum):
    RAISED = 0
    FLAT = 1
    HIDDEN = 2


class TimerStateChange(Enum):
    START = 0
    STOP = 1

class PauseAvailability(Enum):
    ENABLED = 0
    DISABLED = 1
