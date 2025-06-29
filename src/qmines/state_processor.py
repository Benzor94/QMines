from enum import Enum

from PySide6.QtCore import QObject, Signal

class State(Enum):
    INACTIVE = 'Click a tile to start the game'
    ACTIVE = 'Game in progress'
    PAUSED = 'Paused'
    WIN = 'Game finished (win)'
    LOSS = 'Game finished (loss)'

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

    state_change = Signal(State)
    
    def __init__(self):
        super().__init__()
        self._state = State.INACTIVE
    
    @property
    def state(self) -> State:
        return self._state
    
    @state.setter
    def state(self, value: State) -> None:
        self._state = value
        self.state_change.emit(self.state)