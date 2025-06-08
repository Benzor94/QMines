import PySide6.QtWidgets as QW

from qmines.utilities import set_font_size_based_on_height

class PauseButton(QW.QPushButton):
    
    def __init__(self) -> None:
        super().__init__()
        self.setSizePolicy(QW.QSizePolicy.Policy.Minimum, QW.QSizePolicy.Policy.Minimum)
        # set_font_size_based_on_height(self, self.size().height())
        self.setText('Pause')