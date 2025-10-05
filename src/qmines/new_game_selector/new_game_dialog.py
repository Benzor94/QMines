from PySide6.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QLayout, QVBoxLayout, QWidget

from qmines.config import EASY_CONFIG, HARD_CONFIG, MEDIUM_CONFIG, Config
from qmines.new_game_selector.buttons import ModeSelectorButton
from qmines.new_game_selector.custom_mode_selector import CustomModeSelector


class NewGameDialog(QDialog):
    def __init__(self, parent: QWidget | None, config: Config) -> None:
        super().__init__(parent)
        self.setWindowTitle('Set Up New Game')
        self._easy_mode_button = ModeSelectorButton(ModeSelectorButton.Mode.EASY)
        self._medium_mode_button = ModeSelectorButton(ModeSelectorButton.Mode.MEDIUM)
        self._hard_mode_button = ModeSelectorButton(ModeSelectorButton.Mode.HARD)
        self._custom_mode_button = ModeSelectorButton(ModeSelectorButton.Mode.CUSTOM)
        self._buttonbox = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        self._custom_mode_selector = CustomModeSelector(config)
        self._set_layout_properties()
        self._set_up_connections()
        self._selected_config = config

    @property
    def selected_config(self) -> Config:
        return self._selected_config

    def _set_layout_properties(self) -> None:
        mode_selector_button_layout = QHBoxLayout()
        mode_selector_button_layout.addWidget(self._easy_mode_button)
        mode_selector_button_layout.addWidget(self._medium_mode_button)
        mode_selector_button_layout.addWidget(self._hard_mode_button)
        mode_selector_button_layout.addWidget(self._custom_mode_button)
        dialog_layout = QVBoxLayout()
        dialog_layout.addLayout(mode_selector_button_layout)
        dialog_layout.addWidget(self._custom_mode_selector)
        dialog_layout.addWidget(self._buttonbox)
        dialog_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.setLayout(dialog_layout)

    def _set_up_connections(self) -> None:
        self._custom_mode_button.toggled.connect(self._custom_mode_selector.setVisible)
        self._easy_mode_button.clicked.connect(lambda: self._on_mode_selected(EASY_CONFIG))
        self._medium_mode_button.clicked.connect(lambda: self._on_mode_selected(MEDIUM_CONFIG))
        self._hard_mode_button.clicked.connect(lambda: self._on_mode_selected(HARD_CONFIG))
        self._custom_mode_selector.start_button.clicked.connect(lambda: self._on_mode_selected(self._custom_mode_selector.current_config))
        self._buttonbox.rejected.connect(self.reject)

    def _on_mode_selected(self, config: Config) -> None:
        self._selected_config = config
        self.accept()
