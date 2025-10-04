from enum import Enum

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction

from qmines.common import get_qicon_from_path, get_resources_dir


class NewGameAction(QAction):
    ICON = get_resources_dir() / 'plus16.png'

    def __init__(self) -> None:
        super().__init__()
        self.setIcon(get_qicon_from_path(self.ICON))
        self.setText('New')
        self.setToolTip('Start a new game')


class ResetGameAction(QAction):
    ICON = get_resources_dir() / 'reset16.png'

    def __init__(self) -> None:
        super().__init__()
        self.setIcon(get_qicon_from_path(self.ICON))
        self.setText('Reset')
        self.setToolTip('Start over the game with the same settings')


class PauseAction(QAction):
    PAUSE_ICON = get_resources_dir() / 'pause16.png'
    PLAY_ICON = get_resources_dir() / 'play16.png'

    class State(Enum):
        PAUSE = 0
        PLAY = 1

    def __init__(self) -> None:
        super().__init__()
        self._pause_icon = get_qicon_from_path(self.PAUSE_ICON)
        self._play_icon = get_qicon_from_path(self.PLAY_ICON)
        self.setIcon(self._pause_icon)
        self.setText('Pause')
        self.setToolTip('Pause/resume the game')
        self.setCheckable(True)
        self.setEnabled(False)
        self.toggled.connect(self.on_checked)

    @Slot(bool)
    def on_checked(self, checked: bool) -> None:
        self.setIcon(self._play_icon if checked else self._pause_icon)
        self.setText('Resume' if checked else 'Pause')

    def set_icon_state(self, state: State) -> None:
        cls = self.__class__
        match state:
            case cls.State.PAUSE:
                self.setIcon(self._pause_icon)
            case cls.State.PLAY:
                self.setIcon(self._play_icon)


class QuitAction(QAction):
    ICON = get_resources_dir() / 'cross16.png'

    def __init__(self) -> None:
        super().__init__()
        self.setIcon(get_qicon_from_path(self.ICON))
        self.setText('Quit')
        self.setToolTip('Quit the game')


class AboutAction(QAction):
    ICON = get_resources_dir() / 'info16.png'

    def __init__(self) -> None:
        super().__init__()
        self.setIcon(get_qicon_from_path(self.ICON))
        self.setText('About')
        self.setToolTip('Display information')
