from typing import Final

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QSpinBox

from qmines.constants import DEFAULT_TIME_LIMIT, MAXIMUM_TIME_LIMIT, MINIMUM_TIME_LIMIT
from qmines.state.state_manager import StateManager


class HardcoreModeCheckbox(QCheckBox):
    TEXT: Final[str] = 'Time limit'

    def __init__(self):
        super().__init__(self.TEXT)
        self._config = StateManager().config
        self.setChecked(bool(self._config.time_limit))


class HardcoreModeSpinbox(QSpinBox):
    def __init__(self):
        super().__init__()
        self._config = StateManager().config
        self.setMinimum(MINIMUM_TIME_LIMIT)
        self.setMaximum(MAXIMUM_TIME_LIMIT)
        self.setSuffix(' s')
        self.setValue(self._get_time_limit())
        self.setEnabled(bool(self._config.time_limit))

    def _get_time_limit(self) -> int:
        time_limit = self._config.time_limit
        return time_limit if MINIMUM_TIME_LIMIT <= time_limit <= MAXIMUM_TIME_LIMIT else DEFAULT_TIME_LIMIT


class HardcoreModeSelectorLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self._checkbox = HardcoreModeCheckbox()
        self._spinbox = HardcoreModeSpinbox()
        self.addWidget(self.checkbox)
        self.addWidget(self.spinbox)
        self._set_up_connections()

    @property
    def checkbox(self) -> HardcoreModeCheckbox:
        return self._checkbox

    @property
    def spinbox(self) -> HardcoreModeSpinbox:
        return self._spinbox

    @property
    def is_hardcore(self) -> bool:
        return self.checkbox.isChecked()

    @property
    def time_limit(self) -> int:
        return self.spinbox.value() if self.is_hardcore else 0

    @Slot(Qt.CheckState)
    def on_check_state_change(self, check_state: Qt.CheckState) -> None:
        self.spinbox.setEnabled(check_state == Qt.CheckState.Checked)

    def _set_up_connections(self) -> None:
        self.checkbox.checkStateChanged.connect(self.on_check_state_change)
