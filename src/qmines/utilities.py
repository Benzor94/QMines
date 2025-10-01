from importlib.resources import as_file, files
from pathlib import Path

from PySide6.QtGui import QAction, QFont, QIcon
from PySide6.QtWidgets import QWidget


def set_font_size_based_on_height(widget: QWidget | QAction, height: int) -> None:
    new_size = height // 2
    current_font = widget.font()
    if current_font.pointSize() != new_size:
        widget.setFont(QFont(current_font.family(), new_size))

def get_resources_dir() -> Path:
    resources_dir_traversable = files('qmines') / 'resources'
    with as_file(resources_dir_traversable) as resources_dir_path:
        return resources_dir_path

def get_qicon_from_path(path: Path) -> QIcon:
    return QIcon(str(path.resolve()))
