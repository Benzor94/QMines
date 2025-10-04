from PySide6.QtWidgets import QMenuBar

from qmines.controls.actions import AboutAction, NewGameAction, PauseAction, QuitAction, ResetGameAction


class MenuBar(QMenuBar):

    def __init__(self) -> None:
        super().__init__()
        self._new_game = NewGameAction()
        self._reset = ResetGameAction()
        self._pause = PauseAction()
        self._quit = QuitAction()
        self._about = AboutAction()
    
    @property
    def new_game(self) -> NewGameAction:
        return self._new_game
    
    @property
    def reset_game(self) -> ResetGameAction:
        return self._reset
    
    @property
    def pause_game(self) -> PauseAction:
        return self._pause
    
    @property
    def quit(self) -> QuitAction:
        return self._quit
    
    @property
    def about(self) -> AboutAction:
        return self._about
    
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
    