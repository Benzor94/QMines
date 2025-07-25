from PySide6.QtCore import QObject, QSize, Slot
from PySide6.QtWidgets import QFrame, QMainWindow, QSizePolicy, QVBoxLayout

from qmines.board.board import Board
from qmines.dialog.game_over.game_over_dialog import GameOverDialog
from qmines.dialog.new_game.new_game_dialog import NewGameDialog
from qmines.state.config import Config, write_config_to_user_config_dir
from qmines.state.singleton import Singleton
from qmines.state.state_manager import State, StateManager
from qmines.status_bar.status_bar import StatusBar
from qmines.toolbar.toolbar import Toolbar


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._state_manager = StateManager()
        self._config = self._state_manager.config

        self._toolbar = self._create_toolbar()
        self._status_bar = self._create_status_bar()
        self._frame = QFrame()
        self._board = self._create_board()
        self._set_layout()
        self._set_size_properties()
        self.setCentralWidget(self._frame)
        self._set_up_connections()
        self.show()

    @Slot()
    def on_board_reappearing(self) -> None:
        self._adjust_size()

    @Slot()
    def on_game_over_dialog_accepted(self) -> None:
        NewGameDialog(self).exec()

    @Slot(State, State)
    def on_state_change(self, _, current: State) -> None:
        match current:
            case State.WIN | State.LOSS_MINE_HIT | State.LOSS_TIMEOUT:
                dialog = self._create_game_over_dialog()
                dialog.update_label_text()
                dialog.exec()

    def _create_toolbar(self) -> Toolbar:
        toolbar = Toolbar()
        self.addToolBar(toolbar)
        return toolbar

    def _create_status_bar(self) -> StatusBar:
        status_bar = StatusBar()
        self.setStatusBar(status_bar)
        return status_bar

    def _create_board(self) -> Board:
        board = Board()
        board.board_reappeared.connect(self.on_board_reappearing)
        return board

    def _create_game_over_dialog(self) -> GameOverDialog:
        dialog = GameOverDialog(self)
        dialog.accepted.connect(self.on_game_over_dialog_accepted)
        return dialog

    def _set_layout(self) -> None:
        frame_layout = QVBoxLayout()
        frame_layout.addWidget(self._board)
        self._frame.setLayout(frame_layout)

    def _set_size_properties(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    def _adjust_size(self) -> None:
        size = self.size()
        height = size.height()
        width = size.width()
        self.resize(QSize(width + 1, height + 1))
        self.resize(QSize(width, height))

    def _set_up_connections(self) -> None:
        self._state_manager.state_change.connect(self.on_state_change)


class MainWindowManager(QObject, metaclass=Singleton):
    def __init__(self) -> None:
        super().__init__()
        self._state_manager = StateManager()
        self._main_window: MainWindow | None = None
        self._state_manager.new_game_start.connect(self.on_new_game_start)

    def create_main_window(self) -> None:
        if self._main_window is None:
            self._main_window = MainWindow()

    def replace_main_window(self) -> None:
        if self._main_window is None:
            self.create_main_window()
            return
        self._main_window = None
        self.create_main_window()

    @Slot(Config)
    def on_new_game_start(self, config: Config) -> None:
        write_config_to_user_config_dir(config)
        self._state_manager.reset(config)
        self.replace_main_window()
