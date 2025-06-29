from enum import Enum

import PySide6.QtWidgets as QW
import PySide6.QtCore as QC
from PySide6.QtCore import Signal

from qmines.state_processor import State, StateProcessor
from qmines.utilities.constants import BOARD_MIN_LENGTH, BOARD_MAX_LENGTH, PREFERRED_MINE_DENSITY, DEFAULT_TIME_LIMIT, \
    MINIMUM_TIME_LIMIT, MAXIMUM_TIME_LIMIT, EASY_SETTINGS, MEDIUM_SETTINGS, HARD_SETTINGS
from qmines.game_parameters.game_parameters import GameParameters

class GameMode(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2

class NewGameDialog(QW.QDialog):
    EASY_TEXT = 'Easy\n(8 x 8, 10 mines)'
    MED_TEXT = 'Medium\n(16 x 16, 40 mines)'
    HARD_TEXT = 'Hard\n(30 x 16, 99 mines)'
    CUSTOM_TEXT = 'Custom\n(Set manually)'

    def __init__(self, parent: QW.QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle('Set Up New Game')

        self._state_processor = StateProcessor()
        self._parameters = self._state_processor.parameters
        self._custom_mode_column_value = self._parameters.n_cols
        self._custom_mode_row_value = self._parameters.n_rows
        self._custom_mode_mine_value = self._parameters.n_mines
        self._time_limit_value = self._parameters.time_limit_in_seconds

        self._easy_mode_button = QW.QPushButton(self.__class__.EASY_TEXT)
        self._medium_mode_button = QW.QPushButton(self.__class__.MED_TEXT)
        self._hard_mode_button = QW.QPushButton(self.__class__.HARD_TEXT)
        self._custom_mode_button = QW.QPushButton(self.__class__.CUSTOM_TEXT)

        self._custom_mode_frame = QW.QFrame()
        self._custom_mode_column_label = QW.QLabel('Columns: ')
        self._custom_mode_column_spinbox = QW.QSpinBox()
        self._custom_mode_row_label = QW.QLabel('Rows: ')
        self._custom_mode_row_spinbox = QW.QSpinBox()
        self._custom_mode_mine_label = QW.QLabel('Mines: ')
        self._custom_mode_mine_spinbox = QW.QSpinBox()
        self._custom_mode_start_button = QW.QPushButton('Start custom game')

        self._buttonbox = QW.QDialogButtonBox(QW.QDialogButtonBox.StandardButton.Cancel)
        self._buttonbox.rejected.connect(self.reject)

        self._hardcore_mode_checkbox = QW.QCheckBox('Time limit')
        self._hardcore_mode_spinbox = QW.QSpinBox()

        self._set_up_mode_selector_buttons()
        self._set_up_custom_mode_selector()
        self._set_up_hardcore_mode_selector()
        self._set_up_layout()

    def _set_up_custom_mode_selector(self) -> None:
        self._custom_mode_column_spinbox.setMinimum(BOARD_MIN_LENGTH)
        self._custom_mode_column_spinbox.setMaximum(BOARD_MAX_LENGTH)
        self._custom_mode_column_spinbox.setValue(self._custom_mode_column_value)

        self._custom_mode_row_spinbox.setMinimum(BOARD_MIN_LENGTH)
        self._custom_mode_row_spinbox.setMaximum(BOARD_MAX_LENGTH)
        self._custom_mode_row_spinbox.setValue(self._custom_mode_row_value)

        self._custom_mode_mine_spinbox.setMinimum(1)
        self._custom_mode_mine_spinbox.setMaximum(self._parameters.number_of_elements - 1)
        self._custom_mode_mine_spinbox.setValue(self._custom_mode_mine_value)

        self._custom_mode_column_spinbox.valueChanged.connect(self.on_custom_mode_column_number_change)
        self._custom_mode_row_spinbox.valueChanged.connect(self.on_custom_mode_row_number_change)
        self._custom_mode_mine_spinbox.valueChanged.connect(self.on_custom_mode_mine_number_change)

    def _set_up_mode_selector_buttons(self) -> None:
        self._easy_mode_button.clicked.connect(self.on_easy_mode_button_click)
        self._medium_mode_button.clicked.connect(self.on_medium_mode_button_click)
        self._hard_mode_button.clicked.connect(self.on_hard_mode_button_click)
        self._custom_mode_start_button.clicked.connect(self.on_custom_mode_start_button_click)

        self._custom_mode_button.setCheckable(True)
        self._custom_mode_button.toggled.connect(self._custom_mode_frame.setVisible)

    def _set_up_hardcore_mode_selector(self) -> None:
        hardcore_mode = bool(self._time_limit_value)
        self._hardcore_mode_checkbox.setChecked(bool(self._time_limit_value))
        self._hardcore_mode_spinbox.setMinimum(MINIMUM_TIME_LIMIT)
        self._hardcore_mode_spinbox.setMaximum(MAXIMUM_TIME_LIMIT)
        self._hardcore_mode_spinbox.setSuffix(' s')
        self._hardcore_mode_spinbox.setValue(self._get_time_limit_value())
        self._hardcore_mode_spinbox.setEnabled(hardcore_mode)
        self._hardcore_mode_spinbox.valueChanged.connect(self.on_time_limit_value_change)
        self._hardcore_mode_checkbox.checkStateChanged.connect(self.on_hardcore_mode_check_state_change)

    def _set_up_layout(self) -> None:
        mode_layout = QW.QHBoxLayout()
        mode_layout.addWidget(self._easy_mode_button)
        mode_layout.addWidget(self._medium_mode_button)
        mode_layout.addWidget(self._hard_mode_button)
        mode_layout.addWidget(self._custom_mode_button)

        custom_layout = QW.QGridLayout()
        custom_layout.addWidget(self._custom_mode_column_label, 0, 0)
        custom_layout.addWidget(self._custom_mode_column_spinbox, 0, 1)
        custom_layout.addWidget(self._custom_mode_row_label, 1, 0)
        custom_layout.addWidget(self._custom_mode_row_spinbox, 1, 1)
        custom_layout.addWidget(self._custom_mode_mine_label, 2, 0)
        custom_layout.addWidget(self._custom_mode_mine_spinbox, 2, 1)
        custom_layout.addWidget(self._custom_mode_start_button, 3, 1, 1, 2)
        self._custom_mode_frame.setLayout(custom_layout)
        self._custom_mode_frame.setVisible(False)

        hc_mode_layout = QW.QHBoxLayout()
        hc_mode_layout.addWidget(self._hardcore_mode_checkbox)
        hc_mode_layout.addWidget(self._hardcore_mode_spinbox)

        layout = QW.QVBoxLayout()
        layout.setSizeConstraint(QW.QLayout.SizeConstraint.SetFixedSize)
        layout.addLayout(mode_layout)
        layout.addLayout(hc_mode_layout)
        layout.addWidget(self._custom_mode_frame)
        layout.addWidget(self._buttonbox)
        self.setLayout(layout)

    @QC.Slot(int)
    def on_custom_mode_row_number_change(self, value: int):
        self._custom_mode_row_value = value
        self._update_mine_count_upper_limit()

    @QC.Slot(int)
    def on_custom_mode_column_number_change(self, value: int):
        self._custom_mode_column_value = value
        self._update_mine_count_upper_limit()

    @QC.Slot(int)
    def on_custom_mode_mine_number_change(self, value: int):
        self._custom_mode_mine_value = value

    @QC.Slot(QC.Qt.CheckState)
    def on_hardcore_mode_check_state_change(self, check_state: QC.Qt.CheckState) -> None:
        match check_state:
            case QC.Qt.CheckState.Checked:
                self._hardcore_mode_spinbox.setEnabled(True)
                self._time_limit_value = self._hardcore_mode_spinbox.value()
            case QC.Qt.CheckState.Unchecked | QC.Qt.CheckState.PartiallyChecked:
                self._hardcore_mode_spinbox.setEnabled(False)
                self._time_limit_value = 0

    @QC.Slot(int)
    def on_time_limit_value_change(self, value: int) -> None:
        self._time_limit_value = value

    @QC.Slot()
    def on_easy_mode_button_click(self) -> None:
        self._on_new_game_button_click(self._get_parameters_for_named_mode(GameMode.EASY))

    @QC.Slot()
    def on_medium_mode_button_click(self) -> None:
        self._on_new_game_button_click(self._get_parameters_for_named_mode(GameMode.MEDIUM))

    @QC.Slot()
    def on_hard_mode_button_click(self) -> None:
        self._on_new_game_button_click(self._get_parameters_for_named_mode(GameMode.HARD))

    @QC.Slot()
    def on_custom_mode_start_button_click(self) -> None:
        self._on_new_game_button_click(self._get_parameters_for_custom_mode())

    def _update_mine_count_upper_limit(self) -> None:
        size = self._custom_mode_row_value * self._custom_mode_column_value
        self._custom_mode_mine_spinbox.setMinimum(1)
        self._custom_mode_mine_spinbox.setMaximum(size - 1)
        self._custom_mode_mine_spinbox.setValue(round(size * PREFERRED_MINE_DENSITY))

    def _get_time_limit_value(self) -> int:
        return self._time_limit_value if self._time_limit_value >= MINIMUM_TIME_LIMIT else DEFAULT_TIME_LIMIT

    def _get_parameters_for_named_mode(self, mode: GameMode) -> GameParameters:
        initial_dict = {}  # Because of a Pycharm bug
        match mode:
            case GameMode.EASY:
                initial_dict = EASY_SETTINGS
            case GameMode.MEDIUM:
                initial_dict = MEDIUM_SETTINGS
            case GameMode.HARD:
                initial_dict = HARD_SETTINGS
        params = GameParameters.from_dict(initial_dict, time_limit=self._time_limit_value)
        return params

    def _get_parameters_for_custom_mode(self) -> GameParameters:
        return GameParameters(n_rows=self._custom_mode_row_value,
                              n_cols=self._custom_mode_column_value,
                              n_mines=self._custom_mode_mine_value,
                              time_limit_in_seconds=self._time_limit_value)

    def _on_new_game_button_click(self, parameters: GameParameters) -> None:
        self._state_processor.parameters = parameters
        self._state_processor.state = State.INACTIVE
        self.accept()

# TODO: Parameter saving