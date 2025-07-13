from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QApplication

from qmines.main_window import MainWindow
from qmines.state.config import Config, read_config_from_user_config_dir, write_config_to_user_config_dir
from qmines.state.singleton import Singleton
from qmines.state.state_manager import StateManager


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
        old_mw = self._main_window
        self._main_window = None
        old_mw.destroy()
        self.create_main_window()

    @Slot(Config)
    def on_new_game_start(self, config: Config) -> None:
        write_config_to_user_config_dir(config)
        self._state_manager.reset(config)
        self.replace_main_window()


def main() -> None:
    app = QApplication([])
    config = read_config_from_user_config_dir()
    state_manager = StateManager()
    state_manager.config = config
    main_window_manager = MainWindowManager()
    main_window_manager.create_main_window()
    app.exec()
