from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QWidget

from qmines.new_game_selector.buttons import ModeSelectorButton


class NewGameView(QDialog):
    mode_selected = Signal(ModeSelectorButton.Mode)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle('Set Up New Game')
        self._easy_mode_button = ModeSelectorButton(ModeSelectorButton.Mode.EASY)
        self._medium_mode_button = ModeSelectorButton(ModeSelectorButton.Mode.MEDIUM)
        self._hard_mode_button = ModeSelectorButton(ModeSelectorButton.Mode.HARD)
        self._custom_mode_button = ModeSelectorButton(ModeSelectorButton.Mode.CUSTOM)
        self._buttonbox = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        # Connections
        self._easy_mode_button.triggered.connect(self.mode_selected.emit)
        self._medium_mode_button.triggered.connect(self.mode_selected.emit)
        self._hard_mode_button.triggered.connect(self.mode_selected.emit)
