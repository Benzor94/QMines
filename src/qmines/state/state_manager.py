from enum import Enum
from types import MappingProxyType
from typing import override

from PySide6.QtCore import QObject, Signal

from qmines.state.config import Config


class State(Enum):
    INACTIVE = 0
    ACTIVE = 1
    PAUSED = 2
    WIN = 3
    LOSS_MINE_HIT = 4
    LOSS_TIMEOUT = 5

state_text_map = MappingProxyType({State.INACTIVE: 'Click a tile to start',
                                   State.ACTIVE: '',
                                   State.PAUSED: 'Paused',
                                   State.WIN: 'Win',
                                   State.LOSS_MINE_HIT: 'Game over',
                                   State.LOSS_TIMEOUT: 'Game over'})

class FlagCountChange(Enum):
    ADDED = 1
    REMOVED = -1

class Singleton(type(QObject)):
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls.instance = None
    
    @override
    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance

class StateManager(QObject, metaclass=Singleton):

    state_change = Signal(State, State) # Emitted when the game state transitions (previous state, new state)

    def __init__(self):
        super().__init__()
        self._state = State.INACTIVE
        self._config: Config | None = None
        self._revealed_tiles = 0
        self._number_of_flags = 0
    
    @property
    def state(self) -> State:
        return self._state
    
    @state.setter
    def state(self, value: State) -> None:
        previous_state = self._state
        self._state = value
        self.state_change.emit(previous_state, self.state)
    
    @property
    def config(self) -> Config:
        if self._config is None:
            raise ValueError('Game configuration has not been initialized yet.')
        return self._config
    
    @config.setter
    def config(self, value: Config) -> None:
        self._config = value 
    
    def _win_check(self) -> None:
        if self.state == State.ACTIVE:
            config = self.config
            number_of_unrevealed_tiles = config.n_rows * config.n_cols - self._revealed_tiles
            if number_of_unrevealed_tiles == config.n_mines:
                self.state = State.WIN
