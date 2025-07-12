
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar

from qmines.state.state_manager import StateManager
from qmines.toolbar.pause import PauseAction


class Toolbar(QToolBar):

    def __init__(self) -> None:
        super().__init__('Control panel')        
        self._state_manager = StateManager()

        self._new_game_action = self._create_new_game_action()
        self._pause_action = PauseAction()

        self._add_toolbar_buttons()
        self._set_toolbar_properties()    
    
    def _create_new_game_action(self) -> QAction:
        new_game_action = QAction('New')
        new_game_action.setToolTip('Start a new game')
        # Connections
        return new_game_action
    
    def _add_toolbar_buttons(self) -> None:
        self.addAction(self._new_game_action)
        self.addSeparator()
        self.addAction(self._pause_action)
    
    def _set_toolbar_properties(self) -> None:
        self.toggleViewAction().setEnabled(False)
        self.setMovable(False)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
