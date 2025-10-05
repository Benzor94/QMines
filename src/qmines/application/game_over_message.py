from PySide6.QtWidgets import QMessageBox, QPushButton, QWidget

from qmines.common import GameOverReason


class GameOverMessage(QMessageBox):
    def __init__(self, reason: GameOverReason, parent: QWidget) -> None:
        super().__init__(parent)
        self._reason = reason
        self._cancel_button = QPushButton('Cancel')
        self._new_game_button = QPushButton('New game')
        self._reset_button = QPushButton('Reset game')
        self._set_up_text()
        self._set_up_buttons()
        self._set_up_icons()
    
    @property
    def cancel(self) -> QPushButton:
        return self._cancel_button
    
    @property
    def new_game(self) -> QPushButton:
        return self._new_game_button
    
    @property
    def reset(self) -> QPushButton:
        return self._reset_button

    def _set_up_text(self) -> None:
        match self._reason:
            case GameOverReason.WIN:
                text = 'Congratulations, you have won the game!'
                title = 'Game Won'
            case GameOverReason.LOSS:
                text = 'You have lost the game.'
                title = 'Game Lost'
        self.setText(text)
        self.setInformativeText('Do you want to start a new game?')
        self.setWindowTitle(title)

    def _set_up_buttons(self) -> None:
        self.addButton(self._new_game_button, QMessageBox.ButtonRole.AcceptRole)
        self.addButton(self._cancel_button, QMessageBox.ButtonRole.DestructiveRole)
        self.addButton(self._reset_button, QMessageBox.ButtonRole.RejectRole)        

    def _set_up_icons(self) -> None:
        match self._reason:
            case GameOverReason.WIN:
                self.setIcon(QMessageBox.Icon.Question)
            case GameOverReason.LOSS:
                self.setIcon(QMessageBox.Icon.Critical)
