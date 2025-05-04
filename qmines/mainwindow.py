from typing import override
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QApplication, QFrame, QGridLayout, QHBoxLayout, QLayout, QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout
from PySide6.QtCore import QSize, Qt

from qmines.game_parameters import GameParameters
from qmines.board.board_tile import Tile


# class Tile(QPushButton):
#     def __init__(self) -> None:
#         super().__init__()
#         # self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
#         self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    
#     @override
#     def sizeHint(self) -> QSize:
#         return QSize(30, 30)

class GameBoard(QFrame):

    @override
    def resizeEvent(self, event: QResizeEvent):
        size = event.size()
        height = size.height()
        width = size.width()
        smallest = min(height, width)
        self.resize(QSize(smallest, smallest))
         

class MainWindow(QMainWindow):

    def __init__(self, game_parameters: GameParameters) -> None:
        super().__init__()
        self._game_parameters = game_parameters
        # if (layout := self.layout()) is not None:
        #     layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self._set_up()
        self._is_paused = False
    
    def _set_up(self) -> None:
        frame = QFrame()
        frame_layout = QVBoxLayout()
        control_layout = QHBoxLayout()
        board_layout = QGridLayout()

        mine_counter = QPushButton()
        mine_counter.setText('90')
        #mine_counter.setFlat(True)

        new_game_button = QPushButton()
        self.pause_btn = new_game_button
        new_game_button.setText('Pause')
        #new_game_button.setFlat(True)
        new_game_button.clicked.connect(self.on_pause)

        time_tracker = QPushButton()
        time_tracker.setText('32')
        #time_tracker.setFlat(True)

        game_board = GameBoard()
        self.board = game_board
        game_board.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)
        # game_board.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        # sp = game_board.sizePolicy()
        # sp.setRetainSizeWhenHidden(True)
        # game_board.setSizePolicy(sp)
        size_policy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        size_policy.setRetainSizeWhenHidden(True)
        game_board.setSizePolicy(size_policy)
        for i in range(self._game_parameters.n_rows):
            for j in range(self._game_parameters.n_cols):
                board_layout.addWidget(Tile(), i, j)
        board_layout.setSpacing(0)
        board_layout.setContentsMargins(0, 0, 0, 0)
        # board_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        game_board.setLayout(board_layout)

        frame.setLayout(frame_layout)
        control_layout.addWidget(mine_counter)
        control_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.MinimumExpanding))
        control_layout.addWidget(new_game_button)
        control_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.MinimumExpanding))
        control_layout.addWidget(time_tracker)
        frame_layout.addLayout(control_layout)
        frame_layout.addWidget(game_board)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setCentralWidget(frame)
    
    def on_pause(self) -> None:
        if self._is_paused:
            self.board.show()
            self.pause_btn.setText('Pause')
            self._is_paused = False
        else:
            self.board.hide()
            self.pause_btn.setText('Resume')
            self._is_paused = True

if __name__ == '__main__':

    app = QApplication([])
    w = MainWindow(GameParameters(10, 10, n_mines=10))
    w.show()

    app.exec()