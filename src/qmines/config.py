import json
from dataclasses import dataclass
from os import environ
from pathlib import Path
from typing import Final


@dataclass(frozen=True, slots=True)
class Config:
    number_of_rows: int
    number_of_columns: int
    number_of_mines: int


EASY_CONFIG: Final[Config] = Config(8, 8, 10)
MEDIUM_CONFIG: Final[Config] = Config(16, 16, 40)
HARD_CONFIG: Final[Config] = Config(16, 30, 99)


def read_config_from_file() -> Config | None:
    try:
        with open(_get_config_file(), 'r') as f:
            config_json = json.load(f)

        n_rows = config_json['number_of_rows']
        n_cols = config_json['number_of_columns']
        n_mines = config_json['number_of_mines']

        if not isinstance(n_rows, int):
            raise TypeError(f'Number of rows must be integer. Its value was: {n_rows}.')
        if not isinstance(n_cols, int):
            raise TypeError(f'Number of columns must be integer. Its value was: {n_cols}.')
        if not isinstance(n_mines, int):
            raise TypeError(f'Number of mines must be integer. Its value was: {n_mines}.')
        return Config(n_rows, n_cols, n_mines)

    except Exception as e:
        print(f'Something went wrong: {e}. Asking the user for config.')
        return None


def write_config_to_file(config: Config) -> None:
    config_dict = dict(number_of_rows=config.number_of_rows, number_of_columns=config.number_of_columns, number_of_mines=config.number_of_mines)
    config_file = _get_config_file()
    if not (parent := config_file.parent).exists():
        parent.mkdir(parents=True)
    with open(_get_config_file(), 'w') as f:
        json.dump(config_dict, f, indent=2)


def _get_config_dir() -> Path:
    default_conf_dir = environ.get('APPDATA') or environ.get('XDG_CONFIG_HOME')
    return Path(default_conf_dir) / 'QMines' if default_conf_dir else Path.home() / '.config' / 'QMines'


def _get_config_file() -> Path:
    return _get_config_dir() / 'config.json'
