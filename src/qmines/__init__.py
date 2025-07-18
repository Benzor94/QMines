from PySide6.QtWidgets import QApplication

from qmines.main_window import MainWindowManager
from qmines.state.config import read_config_from_user_config_dir
from qmines.state.state_manager import StateManager


def main() -> None:
    app = QApplication([])
    config = read_config_from_user_config_dir()
    state_manager = StateManager()
    state_manager.config = config
    main_window_manager = MainWindowManager()
    main_window_manager.create_main_window()
    app.exec()
