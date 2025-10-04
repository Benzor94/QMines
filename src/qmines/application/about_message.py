from PySide6.QtWidgets import QMessageBox


class AboutMessage(QMessageBox):

    def __init__(self) -> None:
        super().__init__()
        self._set_up_text()
        self._set_up_buttons()
        self._set_up_icons()
    
    def _set_up_text(self) -> None:
        self.setText('[Placeholder]')
        self.setWindowTitle('About')
    
    def _set_up_buttons(self) -> None:
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
    
    def _set_up_icons(self) -> None:
        self.setIcon(QMessageBox.Icon.Information)