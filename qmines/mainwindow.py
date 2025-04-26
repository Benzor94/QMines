from PySide6.QtWidgets import QApplication, QFrame, QGridLayout, QHBoxLayout, QLayout, QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout
from PySide6.QtCore import Qt

from qmines.game_parameters import GameParameters
         

class MainWindow(QMainWindow):

    def __init__(self, game_parameters: GameParameters) -> None:
        super().__init__()
        self._game_parameters = game_parameters
        if (layout := self.layout()) is not None:
            layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self._set_up()
    
    def _set_up(self) -> None:
        frame = QFrame()
        frame_layout = QVBoxLayout()
        control_layout = QHBoxLayout()
        board_layout = QGridLayout()

        mine_counter = QPushButton()
        mine_counter.setText('90')
        mine_counter.setFlat(True)

        new_game_button = QPushButton()
        new_game_button.setText('New Game')
        new_game_button.setFlat(True)

        time_tracker = QPushButton()
        time_tracker.setText('32')
        time_tracker.setFlat(True)

        game_board = QFrame()
        game_board.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)
        game_board.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        board_layout.setSpacing(0)
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
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

if __name__ == '__main__':

    app = QApplication([])
    w = MainWindow(GameParameters(8, 8, n_mines=10))
    w.show()

    app.exec()