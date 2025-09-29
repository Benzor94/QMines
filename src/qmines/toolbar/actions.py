from PySide6.QtGui import QAction, QIcon

from qmines.utilities import get_resources_dir


class NewGameAction(QAction):

    ICON = get_resources_dir() / 'plus16.png'

    def __init__(self) -> None:
        super().__init__()
        self.setIcon(QIcon(str(self.ICON.resolve())))
        self.setToolTip('Start a new game')

class PauseAction(QAction):
    ICON = get_resources_dir() / 'control-pause16.png'

    def __init__(self) -> None:
        super().__init__()
        self.setIcon(QIcon(str(self.ICON.resolve())))
        self.setToolTip('Pause/resume the game')