import PySide6.QtWidgets as QW
import PySide6.QtCore as QC
import PySide6.QtGui as QG
from PySide6.QtCore import Signal

from qmines.constants import BOARD_MIN_SIZE, BOARD_MAX_SIZE, PREFERRED_MINE_DENSITY
from qmines.game_parameters.game_parameters import GameParameters


class NewGameDialog(QW.QDialog):
    EASY_TEXT = 'Easy\n(8 x 8, 10 mines)'
    MED_TEXT = 'Medium\n(16 x 16, 40 mines)'
    HARD_TEXT = 'Hard\n(30 x 16, 99 mines)'
    CUSTOM_TEXT = 'Custom\n(Set manually)'

    start_new_game = Signal()

    def __init__(self, parameters: GameParameters, parent: QW.QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle('Set Up New Game')

        self._parameters = parameters
        self._custom_mode_column_value = self._parameters.n_cols
        self._custom_mode_row_value = self._parameters.n_rows
        self._custom_mode_mine_value = self._parameters.n_mines
        self._timeout_value = self._parameters.timeout_in_seconds

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

        self._hardcore_mode_checkbox = QW.QCheckBox('Hardcore mode')
        self._hardcore_mode_spinbox = QW.QSpinBox()

        self._set_up_mode_selector_buttons()
        self._set_up_custom_mode_selector()
        self._set_up_hardcore_mode_selector()
        self._set_up_layout()

    def _set_up_custom_mode_selector(self) -> None:
        self._custom_mode_column_spinbox.setMinimum(BOARD_MIN_SIZE)
        self._custom_mode_column_spinbox.setMaximum(BOARD_MAX_SIZE)
        self._custom_mode_column_spinbox.setValue(self._custom_mode_column_value)

        self._custom_mode_row_spinbox.setMinimum(BOARD_MIN_SIZE)
        self._custom_mode_row_spinbox.setMaximum(BOARD_MAX_SIZE)
        self._custom_mode_row_spinbox.setValue(self._custom_mode_row_value)

        self._custom_mode_mine_spinbox.setMinimum(1)
        self._custom_mode_mine_spinbox.setMaximum(self._parameters.number_of_elements - 1)
        self._custom_mode_mine_spinbox.setValue(self._custom_mode_mine_value)

        self._custom_mode_column_spinbox.valueChanged.connect(self.on_custom_mode_column_number_change)
        self._custom_mode_row_spinbox.valueChanged.connect(self.on_custom_mode_row_number_change)
        self._custom_mode_mine_spinbox.valueChanged.connect(self.on_custom_mode_mine_number_change)

    def _set_up_mode_selector_buttons(self) -> None:
        self._custom_mode_button.setCheckable(True)
        self._custom_mode_button.toggled.connect(self._custom_mode_frame.setVisible)

    def _set_up_hardcore_mode_selector(self) -> None:
        hardcore_mode = bool(self._timeout_value)
        self._hardcore_mode_checkbox.setChecked(bool(self._timeout_value))
        self._hardcore_mode_spinbox.setMinimum(0)
        self._hardcore_mode_spinbox.setMaximum(3600)
        self._hardcore_mode_spinbox.setSuffix(' s')
        self._hardcore_mode_spinbox.setValue(self._timeout_value)
        self._hardcore_mode_spinbox.setEnabled(hardcore_mode)
        #self._hardcore_mode_checkbox.checkStateChanged.connect(...) # TODO

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
    def on_hardcore_mode_check_state_change(self, check_state: QC.Qt.CheckState): ...

    def _update_mine_count_upper_limit(self) -> None:
        size = self._custom_mode_row_value * self._custom_mode_column_value
        self._custom_mode_mine_spinbox.setMinimum(1)
        self._custom_mode_mine_spinbox.setMaximum(size - 1)
        self._custom_mode_mine_spinbox.setValue(round(size * PREFERRED_MINE_DENSITY))

# TODO: Organize this class properly
# TODO: The hardcore mode spinbox should be disabled unless it is ticked
# TODO: Start making the buttons actually do something. They should fire a new game signal which contains the params
# TODO Cont: received by slot in mainwindow which saves the params to json and reinits mainwindow.