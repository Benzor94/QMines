from enum import Enum
from typing import Final

from PySide6.QtWidgets import QHBoxLayout, QPushButton


class NamedGameMode(Enum):
    EASY = 'Easy\n(8 x 8, 10 mines)'
    MEDIUM = 'Medium\n(16 x 16, 40 mines)'
    HARD = 'Hard\n(30 x 16, 99 mines)'

class NamedGameModeButton(QPushButton):

    def __init__(self, mode: NamedGameMode) -> None:
        super().__init__(mode.value)

class CustomModeButton(QPushButton):

    CUSTOM_MODE_TEXT: Final[str] = 'Custom\n(Set manually)'

    def __init__(self) -> None:
        super().__init__(self.CUSTOM_MODE_TEXT)
        self.setCheckable(True)

class ModeSelectorButtonLayout(QHBoxLayout):
    
    def __init__(self) -> None:
        super().__init__()
        self._easy_mode_button = NamedGameModeButton(NamedGameMode.EASY)
        self._medium_mode_button = NamedGameModeButton(NamedGameMode.MEDIUM)
        self._hard_mode_button = NamedGameModeButton(NamedGameMode.HARD)
        self._custom_mode_button = CustomModeButton()
        self.addWidget(self.easy_mode_button)
        self.addWidget(self.medium_mode_button)
        self.addWidget(self.hard_mode_button)
        self.addWidget(self.custom_mode_button)
    
    @property
    def easy_mode_button(self) -> NamedGameModeButton:
        return self._easy_mode_button
    
    @property
    def medium_mode_button(self) -> NamedGameModeButton:
        return self._medium_mode_button
    
    @property
    def hard_mode_button(self) -> NamedGameModeButton:
        return self._hard_mode_button
    
    @property
    def custom_mode_button(self) -> CustomModeButton:
        return self._custom_mode_button