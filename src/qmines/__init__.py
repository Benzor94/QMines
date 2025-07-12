
from qmines.application import Application
from qmines.state.config import read_config_from_user_config_dir
from qmines.state.state_manager import StateManager


def main() -> None:

    app = Application([])
    config = read_config_from_user_config_dir()
    state_manager = StateManager()
    state_manager.config = config
    app.create_main_window()
    app.exec()
