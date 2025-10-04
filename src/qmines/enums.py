from enum import Enum


class GameOverReason(Enum):
    WIN = 0
    LOSS = 1


class FlagCountChange(Enum):
    ADDED = 1
    REMOVED = -1


class IconState(Enum):
    # To be made internal
    EMPTY = 0
    FLAG = 1
    MINE = 2
    EXPLOSION = 3


class PressedState(Enum):
    # To be made internal
    RAISED = 0
    FLAT = 1
    HIDDEN = 2


class TimerStateChange(Enum):
    # May be made internal
    START = 0
    STOP = 1

class PauseAvailability(Enum):
    # May be made internal
    ENABLED = 0
    DISABLED = 1
