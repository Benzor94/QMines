import unittest
from pathlib import Path

from qmines.constants import EASY_SETTINGS
from qmines.state.config import Config, get_user_config_dir, read_config_from_file, read_config_from_user_config_dir, write_config_to_file, write_config_to_user_config_dir


class TestConfig(unittest.TestCase):
    def test_config_init(self) -> None:
        n_rows = 12
        n_cols = 12
        n_mines = 15
        time_limit = 30

        config = Config(n_rows, n_cols, n_mines, time_limit)
        self.assertEqual(config.n_rows, n_rows)
        self.assertEqual(config.n_cols, n_cols)
        self.assertEqual(config.n_mines, n_mines)
        self.assertEqual(config.time_limit, time_limit)

    def test_config_init_bad_lengths(self) -> None:
        with self.assertRaises(ValueError) as context:
            Config(10, 40, 5, 30)
            self.assertTrue('Board length' in str(context.exception))

        with self.assertRaises(ValueError) as context:
            Config(2, 20, 10, 50)
            self.assertTrue('Board length' in str(context.exception))

    def test_config_init_bad_mines(self) -> None:
        with self.assertRaises(ValueError) as context:
            Config(10, 10, 0, 60)
            self.assertTrue('Mine number' in str(context.exception))

        with self.assertRaises(ValueError) as context:
            Config(10, 10, 100, 60)
            self.assertTrue('Mine number' in str(context.exception))

    def test_config_init_bad_time_limit(self) -> None:
        with self.assertRaises(ValueError) as context:
            Config(8, 8, 10, 9)
            self.assertTrue('Time limit' in str(context.exception))

        with self.assertRaises(ValueError) as context:
            Config(8, 8, 10, 3601)
            self.assertTrue('Time limit' in str(context.exception))

        config = Config(8, 8, 10, 0)
        self.assertEqual(config.time_limit, 0)

    def test_config_read_write_to_json(self) -> None:
        config = Config(12, 12, 15, 120)
        path = Path('./test_data/settings/settings_write_test.json')
        write_config_to_file(path, config)
        read_config = read_config_from_file(path)
        self.assertEqual(config.n_rows, read_config.n_rows)
        self.assertEqual(config.n_cols, read_config.n_cols)
        self.assertEqual(config.n_mines, read_config.n_mines)
        self.assertEqual(config.time_limit, read_config.time_limit)
        path.unlink()

    def test_config_read_write_to_user_config_dir(self) -> None:
        config = Config(12, 12, 15, 120)
        write_config_to_user_config_dir(config)
        read_config = read_config_from_user_config_dir()
        (get_user_config_dir() / 'config.json').unlink()
        self.assertEqual(read_config, config)

    def test_config_read_missing_config(self) -> None:
        conf_file = get_user_config_dir() / 'config.json'
        conf_file.unlink() if conf_file.exists() else None
        config = read_config_from_user_config_dir()
        self.assertEqual(config, Config.from_dict(EASY_SETTINGS))


if __name__ == '__main__':
    unittest.main()
