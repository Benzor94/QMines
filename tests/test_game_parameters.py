import unittest

from qmines.game_parameters.game_parameters import GameParameters
from qmines.game_parameters.settings_reader import read_settings

class TestSettingsReader(unittest.TestCase):

    def test_settings_reading(self) -> None:
        params = read_settings()
        self.assertEqual(params.n_rows, 8)
        self.assertEqual(params.n_cols, 8)
        self.assertEqual(params.n_mines, 10)
        self.assertEqual(params.number_of_elements, 64)
        self.assertEqual(params.timeout_in_seconds, 300)
        self.assertTrue(params.is_hardcore_mode)
    
    def test_game_parameters_exceptions(self) -> None:
        with self.assertRaises(ValueError):
            GameParameters(2, 8, 7, 300)
        
        with self.assertRaises(ValueError):
            GameParameters(5, 1, 3, 200)
        
        with self.assertRaises(ValueError):
            GameParameters(8, 8, 64, 100)
        
        with self.assertRaises(ValueError):
            GameParameters(8, 8, 10, -20)
    


if __name__ == '__main__':
    unittest.main()
