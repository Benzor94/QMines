import unittest
from collections.abc import Sequence

from qmines.utilities import convert_coordinates_to_index, convert_index_to_coordinates, proximity_iterator, range_as_cls_interval, wrap_coordinates, wrap_index


class TestUtilities(unittest.TestCase):

    def test_range_as_cls_interval(self) -> None:
        interval_string = range_as_cls_interval(range(10, 201))
        exp_interval_string = '[10, 200]'
        self.assertEqual(interval_string, exp_interval_string)
    
    def test_wrap_index(self) -> None:
        length = 10
        idxs = list(range(-10, 10))
        wrapped_idxs = [wrap_index(idx, length) for idx in idxs]
        exp_wrapped_idxs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(wrapped_idxs, exp_wrapped_idxs)
    
    def test_wrap_index_exc(self) -> None:
        length = 10
        bad_idxs = [10, -11, 12, -101]
        with self.assertRaises(ValueError) as context:
            wrap_index(bad_idxs[0], length)
            self.assertTrue('must be in range' in str(context.exception))
        with self.assertRaises(ValueError) as context:
            wrap_index(bad_idxs[1], length)
            self.assertTrue('must be in range' in str(context.exception))
        with self.assertRaises(ValueError) as context:
            wrap_index(bad_idxs[2], length)
            self.assertTrue('must be in range' in str(context.exception))
        with self.assertRaises(ValueError) as context:
            wrap_index(bad_idxs[3], length)
            self.assertTrue('must be in range' in str(context.exception))
        
    
    def test_convert_index_to_coordinates(self) -> None:
        n_rows = 3
        n_cols = 4
        idxs = list(range(0, 12))
        coords = [convert_index_to_coordinates(idx, n_rows, n_cols) for idx in idxs]
        exp_coords = [(0, 0), (0, 1), (0, 2), (0, 3),
                      (1, 0), (1, 1), (1, 2), (1, 3),
                      (2, 0), (2, 1), (2, 2), (2, 3)]
        self.assertEqual(coords, exp_coords)
    
    def test_convert_coordinates_to_index(self) -> None:
        n_rows = 3
        n_cols = 4
        coords = [(0, 0), (0, 1), (0, 2), (0, 3),
                  (1, 0), (1, 1), (1, 2), (1, 3),
                  (2, 0), (2, 1), (2, 2), (2, 3)]
        idxs = [convert_coordinates_to_index(row, col, n_rows, n_cols) for row, col in coords]
        exp_idxs = list(range(0, 12))
        self.assertEqual(idxs, exp_idxs)
    
    def test_proximity_iterator(self) -> None:

        class GridImpl:
            def __init__(self, n_rows: int, n_cols: int, words: Sequence[str]) -> None:
                self._n_rows = n_rows
                self._n_cols = n_cols
                self._words = words
                assert len(self._words) == self.n_rows * self.n_cols
            
            @property
            def n_rows(self) -> int:
                return self._n_rows
            @property
            def n_cols(self) -> int:
                return self._n_cols
            def __getitem__(self, coordinates: tuple[int, int]) -> str:
                row, col = wrap_coordinates(*coordinates, self.n_rows, self.n_cols)
                return self._words[convert_coordinates_to_index(row, col, self.n_rows, self.n_cols)]
        
        grid = GridImpl(3, 4, ['a', 'b', 'c', 'd',
                               'e', 'f', 'g', 'h',
                               'i', 'j', 'k', 'l'])
        corner_iteration = {e for e in proximity_iterator(grid, 0, 3)}
        exp_corner_iteration = {'c', 'g', 'h'}
        edge_iteration = {e for e in proximity_iterator(grid, 1, 0)}
        exp_edge_iteration = {'a', 'b', 'f', 'j', 'i'}
        interior_iteration = {e for e in proximity_iterator(grid, 1, 2)}
        exp_interior_iteration = {'b', 'c', 'd', 'f', 'h', 'j', 'k', 'l'}
        self.assertEqual(corner_iteration, exp_corner_iteration)
        self.assertEqual(edge_iteration, exp_edge_iteration)
        self.assertEqual(interior_iteration, exp_interior_iteration)



if __name__ == '__main__':
    unittest.main()