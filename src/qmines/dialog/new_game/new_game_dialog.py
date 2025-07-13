

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFrame, QLayout, QVBoxLayout, QWidget

from qmines.constants import EASY_SETTINGS, HARD_SETTINGS, MEDIUM_SETTINGS
from qmines.dialog.new_game.custom_mode import CustomModeSettingsLayout
from qmines.dialog.new_game.hardcore_mode import HardcoreModeSelectorLayout
from qmines.dialog.new_game.mode_selector_buttons import ModeSelectorButtonLayout, NamedGameMode
from qmines.state.config import Config
from qmines.state.state_manager import StateManager


class NewGameDialog(QDialog):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Set Up New Game')
        self._state_manager = StateManager()

        self._mode_selector = ModeSelectorButtonLayout()
        self._hardcore_mode_selector = HardcoreModeSelectorLayout()
        self._custom_mode_settings = CustomModeSettingsLayout()
        self._custom_mode_settings_frame = self._create_custom_mode_settings_frame()
        self._buttonbox = self._create_buttonbox()
        self._set_layout_properties()
        self._set_up_connections()
    
    @Slot()
    def on_custom_mode_start_button_click(self) -> None:
        config = Config(n_rows=self._custom_mode_settings.row_number,
                        n_cols=self._custom_mode_settings.column_number,
                        n_mines=self._custom_mode_settings.mine_number,
                        time_limit=self._hardcore_mode_selector.time_limit)
        self._start_new_game(config)
    
    @Slot(NamedGameMode)
    def on_named_mode_button_click(self, mode: NamedGameMode) -> None:
        match mode:
            case NamedGameMode.EASY:
                initial_config_dict = EASY_SETTINGS.copy()
            case NamedGameMode.MEDIUM:
                initial_config_dict = MEDIUM_SETTINGS.copy()
            case NamedGameMode.HARD:
                initial_config_dict = HARD_SETTINGS.copy()
        time_limit = self._hardcore_mode_selector.time_limit
        config = Config.from_dict(initial_config_dict, time_limit=time_limit)
        self._start_new_game(config)    
    
    def _create_custom_mode_settings_frame(self) -> QFrame:
        frame = QFrame()
        frame.setLayout(self._custom_mode_settings)
        frame.setVisible(False)
        return frame
    
    def _create_buttonbox(self) -> QDialogButtonBox:
        buttonbox = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        buttonbox.rejected.connect(self.reject)
        return buttonbox
    
    def _set_layout_properties(self) -> None:
        layout = QVBoxLayout()
        layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        layout.addLayout(self._mode_selector)
        layout.addLayout(self._hardcore_mode_selector)
        layout.addWidget(self._custom_mode_settings_frame)
        layout.addWidget(self._buttonbox)
        self.setLayout(layout)
    
    def _set_up_connections(self) -> None:
        self._mode_selector.custom_mode_button.toggled.connect(self._custom_mode_settings_frame.setVisible)
        self._mode_selector.named_mode_button_clicked.connect(self.on_named_mode_button_click)
        self._custom_mode_settings.start_button.clicked.connect(self.on_custom_mode_start_button_click)
    
    def _start_new_game(self, new_config: Config) -> None:
        self.accept()
        self._state_manager.new_game_start.emit(new_config)