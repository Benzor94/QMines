import PySide6.QtWidgets as QW
from PySide6.QtGui import QFont, QAction


def set_font_size_based_on_height(widget: QW.QWidget | QAction, height: int) -> None:
    new_size = height // 2
    current_font = widget.font()
    if current_font.pointSize() != new_size:
        widget.setFont(QFont(current_font.family(), new_size))