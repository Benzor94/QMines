from collections.abc import Callable

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QHBoxLayout, QLayout, QPushButton, QVBoxLayout, QWidget

from qmines.config import Config
from qmines.new_game_selector.buttons import ModeSelectorButton
from qmines.new_game_selector.custom_mode_selector import BoardLengthSelector, CustomModeSelector, MineCountSelector


class NewGameDialog(QDialog):
    mode_selected = Signal(ModeSelectorButton.Mode)
    board_width_changed = Signal(int)
    board_height_changed = Signal(int)
    mine_count_changed = Signal(int)

    def __init__(
        self,
        parent: QWidget,
        min_board_length: int,
        max_board_length: int,
        min_mine_count: int,
        max_mine_count: Callable[[int], int],
        initial_config: Config,
        preferred_mine_density: float,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle('Set Up New Game')
        self._easy_mode_button = ModeSelectorButton(ModeSelectorButton.Mode.EASY)
        self._medium_mode_button = ModeSelectorButton(ModeSelectorButton.Mode.MEDIUM)
        self._hard_mode_button = ModeSelectorButton(ModeSelectorButton.Mode.HARD)
        self._custom_mode_button = ModeSelectorButton(ModeSelectorButton.Mode.CUSTOM)
        self._buttonbox = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        self._board_height_selector = BoardLengthSelector(BoardLengthSelector.Dimension.HEIGHT, min_board_length, max_board_length, initial_config.number_of_rows)
        self._board_width_selector = BoardLengthSelector(BoardLengthSelector.Dimension.WIDTH, min_board_length, max_board_length, initial_config.number_of_columns)
        self._mine_count_selector = MineCountSelector(
            min_mine_count, max_mine_count, initial_config.number_of_mines, initial_config.number_of_rows * initial_config.number_of_columns, preferred_mine_density
        )
        self._start_custom_game_button = QPushButton('Start custom game')
        self._set_dialog_layout()
        # Connections
        self._easy_mode_button.triggered.connect(self.mode_selected.emit)
        self._medium_mode_button.triggered.connect(self.mode_selected.emit)
        self._hard_mode_button.triggered.connect(self.mode_selected.emit)
        self._buttonbox.rejected.connect(self.reject)
        self._start_custom_game_button.clicked.connect(lambda: self.mode_selected.emit(ModeSelectorButton.Mode.CUSTOM))
        self._board_height_selector.valueChanged.connect(self.board_width_changed.emit)
        self._board_width_selector.valueChanged.connect(self.board_height_changed.emit)
        self._mine_count_selector.valueChanged.connect(self.mine_count_changed.emit)

    @Slot(int)
    def update_max_mine_count(self, value: int) -> None:
        self._mine_count_selector.update_max(value)

    def _set_dialog_layout(self) -> None:
        mode_selector_button_layout = QHBoxLayout()
        mode_selector_button_layout.addWidget(self._easy_mode_button)
        mode_selector_button_layout.addWidget(self._medium_mode_button)
        mode_selector_button_layout.addWidget(self._hard_mode_button)
        mode_selector_button_layout.addWidget(self._custom_mode_button)
        custom_mode_selector = CustomModeSelector(self._board_height_selector, self._board_width_selector, self._mine_count_selector, self._start_custom_game_button)
        self._custom_mode_button.toggled.connect(custom_mode_selector.setVisible)
        dialog_layout = QVBoxLayout()
        dialog_layout.addLayout(mode_selector_button_layout)
        dialog_layout.addWidget(custom_mode_selector)
        dialog_layout.addWidget(self._buttonbox)
        dialog_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.setLayout(dialog_layout)
