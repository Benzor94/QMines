from typing import Final

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QDialog, QWidget

from qmines.config import EASY_CONFIG, HARD_CONFIG, MEDIUM_CONFIG, Config
from qmines.new_game_selector.buttons import ModeSelectorButton
from qmines.new_game_selector.new_game_dialog import NewGameDialog


class NewGameSelector(QObject):

    BOARD_MIN_LENGTH: Final[int] = 10
    BOARD_MAX_LENGTH: Final[int] = 30
    PREFERRED_MINE_DENSITY: Final[float] = 0.156
    MINIMUM_NUMBER_OF_MINES: Final[int] = 8
    MINIMUM_NUMBER_OF_EMPTY_TILES: Final[int] = 25

    start_new_game = Signal(Config)

    def __init__(self, dialog_parent: QWidget, config: Config) -> None:
        super().__init__()
        self._dialog = NewGameDialog(parent=dialog_parent,
                                     min_board_length=self.BOARD_MIN_LENGTH,
                                     max_board_length=self.BOARD_MAX_LENGTH,
                                     min_mine_count=self.MINIMUM_NUMBER_OF_MINES,
                                     max_mine_count=lambda size: size - self.MINIMUM_NUMBER_OF_EMPTY_TILES,
                                     initial_config=config,
                                     preferred_mine_density=self.PREFERRED_MINE_DENSITY)
        self._current_height = config.number_of_rows
        self._current_width = config.number_of_columns
        self._current_mine_number = config.number_of_mines
        # Connections
        self._dialog.board_height_changed.connect(self.on_board_height_changed)
        self._dialog.board_width_changed.connect(self.on_board_width_changed)
        self._dialog.mine_count_changed.connect(self.on_mine_count_changed)
        self._dialog.mode_selected.connect(self.on_mode_selected)
        # Run dialog
        self._result = QDialog.DialogCode(self._dialog.exec())
    
    @property
    def result(self) -> Config | None:
        if self._result == QDialog.DialogCode.Accepted:
            return Config(self._current_height, self._current_width, self._current_mine_number)
        return None

    @Slot(int)
    def on_board_height_changed(self, value: int) -> None:
        self._current_height = value
    
    @Slot(int)
    def on_board_width_changed(self, value: int) -> None:
        self._current_width = value
    
    @Slot(int)
    def on_mine_count_changed(self, value: int) -> None:
        self._current_mine_number = value

    @Slot(ModeSelectorButton.Mode)
    def on_mode_selected(self, mode: ModeSelectorButton.Mode) -> None:
        self._dialog.board_height_changed.disconnect(self.on_board_height_changed)
        self._dialog.board_width_changed.disconnect(self.on_board_width_changed)
        self._dialog.mine_count_changed.disconnect(self.on_mine_count_changed)
        match mode:
            case ModeSelectorButton.Mode.EASY:
                self._current_height = EASY_CONFIG.number_of_rows
                self._current_width = EASY_CONFIG.number_of_columns
                self._current_mine_number = EASY_CONFIG.number_of_mines
            case ModeSelectorButton.Mode.MEDIUM:
                self._current_height = MEDIUM_CONFIG.number_of_rows
                self._current_width = MEDIUM_CONFIG.number_of_columns
                self._current_mine_number = MEDIUM_CONFIG.number_of_mines
            case ModeSelectorButton.Mode.HARD:
                self._current_height = HARD_CONFIG.number_of_rows
                self._current_width = HARD_CONFIG.number_of_columns
                self._current_mine_number = HARD_CONFIG.number_of_mines
        self._dialog.accept()


