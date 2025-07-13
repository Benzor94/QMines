from enum import Enum
from types import MappingProxyType

from PySide6.QtCore import QObject, Signal, Slot

from qmines.state.config import Config
from qmines.state.singleton import Singleton


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

class StateManager(QObject, metaclass=Singleton):

    state_change = Signal(State, State)  # Emitted when the game state transitions (previous state, new state)
    flag_count_change = Signal(FlagCountChange)  # Emitted when a flag is placed or removed
    first_click_in_game = Signal(int, int)  # Emitted when the game is started by making the first click on a tile (coordinates of clicked tile)
    tile_revealed = Signal(int, int)  # Emitted when a hidden tile is revealed (coordinates of the revealed tile)
    revealed_tile_clicked = Signal(int, int)  # Emitted when an already revealed tile is clicked (coordinates of the clicked tile)
    new_game_start = Signal(Config)  # Emitted when a new game is started to destroy then recreate the board (config of the new game)

    def __init__(self):
        super().__init__()
        self._state = State.INACTIVE
        self._config: Config | None = None
        self._revealed_tiles = 0
        self._set_up_connections()
    
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
    
    def reset(self, config: Config) -> None:
        self.config = config
        self._revealed_tiles = 0
        self.state = State.INACTIVE
    
    @Slot(int, int)
    def on_tile_revealed(self) -> None:
        if self.state == State.ACTIVE:
            self._revealed_tiles += 1
            self._win_check()
    
    def _win_check(self) -> None:
        if self.state == State.ACTIVE:
            config = self.config
            number_of_unrevealed_tiles = config.n_rows * config.n_cols - self._revealed_tiles
            if number_of_unrevealed_tiles == config.n_mines:
                self.state = State.WIN

    def _set_up_connections(self) -> None:
        self.tile_revealed.connect(self.on_tile_revealed)