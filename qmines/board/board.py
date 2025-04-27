

from PySide6.QtWidgets import QFrame

from qmines.game_parameters import GameParameters


class Board(QFrame):

    def __init__(self, parameters: GameParameters) -> None:
        super().__init__()
        self._params = parameters
        self._tiles = []
