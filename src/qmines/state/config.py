import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from os import environ
from pathlib import Path
from typing import ClassVar

from qmines.constants import BOARD_MAX_LENGTH, BOARD_MIN_LENGTH, EASY_SETTINGS, MAXIMUM_TIME_LIMIT, MINIMUM_TIME_LIMIT
from qmines.utilities import range_as_cls_interval


@dataclass(slots=True, frozen=True)
class Config:
    LENGTH_RANGE: ClassVar[range] = range(BOARD_MIN_LENGTH, BOARD_MAX_LENGTH + 1)
    TIME_LIMIT_RANGE: ClassVar[range] = range(MINIMUM_TIME_LIMIT, MAXIMUM_TIME_LIMIT + 1)
    n_rows: int
    n_cols: int
    n_mines: int
    time_limit: int

    def __post_init__(self) -> None:
        if (self.n_rows not in self.LENGTH_RANGE) or (self.n_cols not in self.LENGTH_RANGE):
            raise ValueError(f'Board length (specified: n_rows = {self.n_rows}, n_cols = {self.n_cols}) must be in {range_as_cls_interval(self.LENGTH_RANGE)}.')
        mine_range = range(1, self.n_rows * self.n_cols)
        if self.n_mines not in mine_range:
            raise ValueError(f'Mine number (specified: {self.n_mines}) must be in {range_as_cls_interval(mine_range)}.')
        if (self.time_limit not in self.TIME_LIMIT_RANGE) and self.time_limit != 0:
            raise ValueError(f'Time limit (specified: {self.time_limit}) must be in {range_as_cls_interval(self.TIME_LIMIT_RANGE)} or zero.')

    @classmethod
    def from_dict(
        cls,
        dict_: Mapping[str, int],
        *,
        n_rows: int | None = None,
        n_cols: int | None = None,
        n_mines: int | None = None,
        time_limit: int | None = None,
    ) -> 'Config':
        n_rows_ = n_rows if n_rows is not None else dict_.get('n_rows', EASY_SETTINGS['n_rows'])
        n_cols_ = n_cols if n_cols is not None else dict_.get('n_cols', EASY_SETTINGS['n_cols'])
        n_mines_ = n_mines if n_mines is not None else dict_.get('n_mines', EASY_SETTINGS['n_mines'])
        time_limit_ = time_limit if time_limit is not None else dict_.get('time_limit', EASY_SETTINGS['time_limit'])

        return cls(n_rows=n_rows_, n_cols=n_cols_, n_mines=n_mines_, time_limit=time_limit_)

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


def read_config_from_file(path: Path) -> Config:
    with open(path, 'r') as f:
        config_json = json.load(f)
        return Config.from_dict(config_json)

def write_config_to_file(path: Path, config: Config) -> None:
    with open(path, 'w') as f:
        json.dump(config.to_dict(), f, indent=2)

def write_config_to_user_config_dir(config: Config) -> None:
    app_config_dir = get_user_config_dir()
    app_config_dir.mkdir(parents=True, exist_ok=True)
    
    write_config_to_file(app_config_dir / 'config.json', config)

def read_config_from_user_config_dir() -> Config:
    app_config_dir = get_user_config_dir()
    config_file = app_config_dir / 'config.json'
    config = read_config_from_file(config_file) if config_file.is_file() else Config.from_dict(EASY_SETTINGS)
    return config

def get_user_config_dir() -> Path:
    default_conf_dir = environ.get('APPDATA') or environ.get('XDG_CONFIG_HOME')
    return Path(default_conf_dir) if default_conf_dir else Path.home() / '.config' / 'QMines'
