from PySide6.QtWidgets import QMessageBox

from qmines.enums import GameOverReason


class GameOverMessage(QMessageBox):

    def __init__(self, reason: GameOverReason) -> None:
        super().__init__()
        self._reason = reason
        self.setWindowTitle('QMines')
        self._set_up_text()
        self._set_up_buttons()
        self._set_up_icons()
    
    def _set_up_text(self) -> None:
        match self._reason:
            case GameOverReason.WIN:
                text = 'Congratulations, you have won the game!'
            case GameOverReason.LOSS:
                text = 'You have lost the game.'
        self.setText(text)
        self.setInformativeText('Do you want to start a new game?')
    
    def _set_up_buttons(self) -> None:
        self.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    
    def _set_up_icons(self) -> None:
        match self._reason:
            case GameOverReason.WIN:
                self.setIcon(QMessageBox.Icon.Question)
            case GameOverReason.LOSS:
                self.setIcon(QMessageBox.Icon.Critical)


