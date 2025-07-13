
from typing import Final
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt

from qmines.state.state_manager import State, StateManager

class GameOverDialog(QDialog):

    QUESTION_TEXT: Final[str] = '\nWould you like to start a new game?'
    WIN_TEXT: Final[str] = 'Congratulations, you have won the game!'
    LOSS_TEXT: Final[str] = 'You have lost the game!'
    REASON_TEXT_MINE: Final[str] = ' (Mine triggered)'
    REASON_TEXT_TIMEOUT: Final[str] = ' (Time ran out)'

    
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Game Over')

        self._state_manager = StateManager()
        self._label = QLabel('')
        self._buttonbox = self._create_buttonbox()
        self._set_layout_properties()
    
    def _create_buttonbox(self) -> QDialogButtonBox:
        buttonbox = QDialogButtonBox(Qt.Orientation.Horizontal)
        ok_button = QPushButton('New game')
        buttonbox.addButton(ok_button, QDialogButtonBox.ButtonRole.AcceptRole)
        buttonbox.addButton(QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        return buttonbox
    
    def _set_layout_properties(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(self._label)
        layout.addWidget(self._buttonbox)
        self.setLayout(layout)
    
    def update_label_text(self) -> None:
        match self._state_manager.state:
            case State.WIN:
                text = self.WIN_TEXT + self.QUESTION_TEXT
            case State.LOSS_MINE_HIT:
                text = self.LOSS_TEXT + self.REASON_TEXT_MINE + self.QUESTION_TEXT
            case State.LOSS_TIMEOUT:
                text = self.LOSS_TEXT + self.REASON_TEXT_TIMEOUT + self.QUESTION_TEXT
            case _:
                raise ValueError('Game over dialog triggered without the game being over?!')
        self._label.setText(text)
