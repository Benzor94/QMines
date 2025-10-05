from enum import Enum
from threading import Lock

from PySide6.QtCore import QObject, QTimer, Signal, Slot

from qmines.common import FlagCountChange, GameOverReason
from qmines.config import Config
from qmines.controls.actions import AboutAction, NewGameAction, PauseAction, QuitAction, ResetGameAction
from qmines.controls.counters import MineCounter, TimeTracker
from qmines.controls.menubar import MenuBar
from qmines.controls.toolbar import Toolbar


class ControlManager(QObject):
    class TimerStateChange(Enum):
        START = 0
        STOP = 1

    class PauseAvailability(Enum):
        ENABLED = 0
        DISABLED = 1

    new_game = Signal()
    start_over_game = Signal()
    game_paused = Signal(bool)
    game_quit = Signal()
    about_dialog_invoked = Signal()

    def __init__(self, config: Config) -> None:
        super().__init__()
        self._timer = self._create_timer()
        self._new_game_action = NewGameAction()
        self._reset_game_action = ResetGameAction()
        self._pause_action = PauseAction()
        self._quit_action = QuitAction()
        self._about_action = AboutAction()
        self._mine_counter = MineCounter(config.number_of_mines)
        self._time_tracker = TimeTracker()
        self._toolbar = Toolbar(self._new_game_action, self._reset_game_action, self._pause_action, self._mine_counter, self._time_tracker)
        self._menubar = MenuBar(self._new_game_action, self._reset_game_action, self._pause_action, self._quit_action, self._about_action)
        self._lock = Lock()
        self._seconds_elapsed = 0
        self._number_of_remaining_mines = config.number_of_mines
        # Connections
        self._new_game_action.triggered.connect(self.new_game.emit)
        self._reset_game_action.triggered.connect(self.start_over_game.emit)
        self._pause_action.toggled.connect(self.game_paused.emit)
        self._quit_action.triggered.connect(self.game_quit.emit)
        self._about_action.triggered.connect(self.about_dialog_invoked.emit)

    @property
    def toolbar(self) -> Toolbar:
        return self._toolbar

    @property
    def menubar(self) -> MenuBar:
        return self._menubar

    @Slot(TimerStateChange)
    def on_time_tracking_state_change(self, state_change: TimerStateChange) -> None:
        match state_change:
            case self.TimerStateChange.START:
                self._timer.start()
            case self.TimerStateChange.STOP:
                self._timer.stop()

    @Slot(FlagCountChange)
    def on_flag_count_change(self, change: FlagCountChange) -> None:
        with self._lock:
            match change:
                case FlagCountChange.ADDED:
                    self._number_of_remaining_mines -= 1

                case FlagCountChange.REMOVED:
                    self._number_of_remaining_mines += 1
            self._mine_counter.update_counter(self._number_of_remaining_mines)

    @Slot(PauseAvailability)
    def on_pause_availability_change(self, availability: PauseAvailability) -> None:
        match availability:
            case self.PauseAvailability.ENABLED:
                self._pause_action.setEnabled(True)
            case self.PauseAvailability.DISABLED:
                self._pause_action.setEnabled(False)

    @Slot()
    def on_timer_period(self) -> None:
        self._seconds_elapsed += 1
        self._time_tracker.update_counter(self._seconds_elapsed)

    @Slot(GameOverReason)
    def on_game_over(self, reason: GameOverReason) -> None:
        if reason == GameOverReason.WIN:
            self._mine_counter.update_counter(0)

    def _create_timer(self) -> QTimer:
        timer = QTimer()
        timer.setInterval(1000)
        timer.timeout.connect(self.on_timer_period)
        return timer
