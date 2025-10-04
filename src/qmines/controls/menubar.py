from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar


class MenuBar(QMenuBar):

    def __init__(self, new_game: QAction, reset_game: QAction, pause: QAction, quit: QAction, about: QAction) -> None:
        super().__init__()
        self._new_game = new_game
        self._reset = reset_game
        self._pause = pause
        self._quit = quit
        self._about = about
        self._set_game_menu()
        self._set_score_menu()
        self._set_help_menu()
    
    def _set_game_menu(self) -> None:
        game_menu = self.addMenu('Game')
        game_menu.addAction(self._new_game)
        game_menu.addAction(self._reset)
        game_menu.addAction(self._pause)
        game_menu.addSeparator()
        game_menu.addAction(self._quit)
    
    def _set_score_menu(self) -> None:
        _ = self.addMenu('Score')

    
    def _set_help_menu(self) -> None:
        help_menu = self.addMenu('Help')
        help_menu.addAction(self._about)
    