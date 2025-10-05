from enum import Enum
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import as_file, files
from pathlib import Path

from PySide6.QtGui import QIcon


class GameOverReason(Enum):
    WIN = 0
    LOSS = 1


class FlagCountChange(Enum):
    ADDED = 1
    REMOVED = -1


def get_resources_dir() -> Path:
    resources_dir_traversable = files('qmines') / 'resources'
    with as_file(resources_dir_traversable) as resources_dir_path:
        return resources_dir_path


def get_qicon_from_path(path: Path) -> QIcon:
    return QIcon(str(path.resolve()))

def get_version() -> str:
    try:
        ver = version('qmines')
    except PackageNotFoundError:
        ver = 'N/A'
    return ver