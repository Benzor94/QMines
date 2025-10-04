from PySide6.QtWidgets import QMessageBox


class StartOverMessage(QMessageBox):

    def __init__(self, is_game_over: bool) -> None:
        super().__init__()
        if is_game_over:
            self.accept()
        self._set_up_text()
        self._set_up_buttons()
        self._set_up_icons()
    
    def _set_up_text(self) -> None:
        self.setText('Do you want to start over the game?')
        self.setInformativeText('Doing so will erase all progress.')
        self.setWindowTitle('Reset Game')
    
    def _set_up_buttons(self) -> None:
        self.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    
    def _set_up_icons(self) -> None:
        self.setIcon(QMessageBox.Icon.Warning)
