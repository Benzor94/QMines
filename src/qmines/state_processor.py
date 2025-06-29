from enum import Enum

from PySide6.QtCore import QObject, Signal

from qmines.game_parameters.game_parameters import GameParameters

class State(Enum):
    INACTIVE = 'Click a tile to start'
    ACTIVE = ''
    PAUSED = 'Paused'
    WIN = 'Game won'
    LOSS_MINE_HIT = 'Game lost (mine exploded)'
    LOSS_TIMEOUT = 'Game lost (time has run out)'

class FlagCountChange(Enum):
    ADDED = 1
    REMOVED = -1

class Singleton[T]:
    def __init__(self, cls: type[T]):
        self._cls = cls
        self._instance: T | None = None
    
    def __call__(self) -> T:
        if self._instance is None:
            self._instance = self._cls()
        return self._instance

@Singleton
class StateProcessor(QObject):

    state_change = Signal(State, State)  # The game state transitions (previous state, current state)
    first_click = Signal(int, int)  # A tile has been left-clicked for the first time in the game
    tile_revealed = Signal(int, int)  # During an active game, an unrevealed tile is left-clicked
    revealed_tile_clicked = Signal(int, int)  # During an active game, a previously revealed tile is left-clicked
    flag_change = Signal(FlagCountChange)  # During an active game, an unrevealed tile is right-clicked
    
    def __init__(self):
        super().__init__()
        self._state = State.INACTIVE
        self._parameters: GameParameters | None = None
    
    @property
    def state(self) -> State:
        return self._state
    
    @state.setter
    def state(self, value: State) -> None:
        previous_state = self.state
        self._state = value
        self.state_change.emit(previous_state, self.state)
    
    @property
    def parameters(self) -> GameParameters:
        if self._parameters is None:
            raise ValueError('Game parameters have not been initialized.')
        return self._parameters
    
    @parameters.setter
    def parameters(self, value: GameParameters) -> None:
        self._parameters = value