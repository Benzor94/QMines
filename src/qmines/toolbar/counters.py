from PySide6.QtWidgets import QFrame, QHBoxLayout, QLCDNumber, QLabel
from PySide6.QtGui import QIcon

from qmines.utilities import get_resources_dir

class MineCounter(QFrame):

    ICON = get_resources_dir() / 'mine256.png'

    def __init__(self, n_mines: int) -> None:
        super().__init__()
        self._n_mines = n_mines
        self._label = QLabel()
        self._label2 = QLabel(':')
        self._counter = QLCDNumber()

        self._label.setPixmap(QIcon(str(self.ICON.resolve())).pixmap(16, 16))
        #self._label.setStyleSheet("border: 1px solid red;")
        self._counter.display('012')
        #self._counter.setStyleSheet("border: 1px solid red;")
        self._counter.setDigitCount(3)
        self._counter.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._label2)
        self._layout.addWidget(self._counter)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        self.setToolTip('Number of mines remaining')

        #self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        #self.setLineWidth(1)

class TimeTracker(QFrame):

    ICON = get_resources_dir() / 'clock16.png'

    def __init__(self) -> None:
        super().__init__()
        self._label = QLabel()
        self._label2 = QLabel(':')
        self._counter = QLCDNumber()

        self._label.setPixmap(QIcon(str(self.ICON.resolve())).pixmap(16, 16))
        #self._label.setStyleSheet("border: 1px solid red;")
        self._counter.display('012')
        #self._counter.setStyleSheet("border: 1px solid red;")
        self._counter.setDigitCount(3)
        self._counter.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._label2)
        self._layout.addWidget(self._counter)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        self.setToolTip('Seconds elapsed')