from typing import override
from collections.abc import Iterator
import unittest

from qmines.grid.abstract_grid import AbstractGrid

class GridImpl(AbstractGrid[str]):
    
    def __init__(self, n_rows: int, n_cols: int, elements: list[str]) -> None:
        self._n_rows = n_rows
        self._n_cols = n_cols
        self._elements = elements
    
    @property
    @override
    def n_rows(self) -> int:
        return self._n_rows
    
    @property
    @override
    def n_cols(self) -> int:
        return self._n_cols
    
    @override
    def __getitem__(self, coordinates: tuple[int, int]) -> str:
        return self._elements[self.to_index(*coordinates)]
    
    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self._elements)
    
    def _verify_element_length(self) -> None:
        if len(self._elements) != self.number_of_elements:
            raise ValueError("The number of elements does not equal the size of the grid.")

class TestGrid(unittest.TestCase):

    @override
    def setUp(self) -> None:
        self.grid = GridImpl(3, 4, ['a', 'b', 'c', 'd', # pyright: ignore [reportUninitializedInstanceVariable]
                                    'e', 'f', 'g', 'h',
                                    'i', 'j', 'k', 'l'])
    
    def test_properties(self) -> None:
        nrows = self.grid.n_rows
        ncols = self.grid.n_cols
        n_of_elems = self.grid.number_of_elements

        self.assertEqual(nrows, 3)
        self.assertEqual(ncols, 4)
        self.assertEqual(n_of_elems, 12)
    
    def test_itemgetting(self) -> None:
        item1 = self.grid[0, 2]  # c
        item2 = self.grid[1, 0]  # e
        item3 = self.grid[2, 3]  # l

        self.assertEqual(item1, 'c')
        self.assertEqual(item2, 'e')
        self.assertEqual(item3, 'l')
    
    def test_index_wrapping(self) -> None:
        wrapped_index_1 = self.grid.wrap_index(11)
        wrapped_index_2 = self.grid.wrap_index(-12)
        self.assertEqual(wrapped_index_1, 11)
        self.assertEqual(wrapped_index_2, 0)

        wrapped_coords_1 = self.grid.wrap_coordinates(1, 2)
        wrapped_coords_2 = self.grid.wrap_coordinates(2, -4)
        wrapped_coords_3 = self.grid.wrap_coordinates(-2, 3)
        self.assertEqual(wrapped_coords_1, (1, 2))
        self.assertEqual(wrapped_coords_2, (2, 0))
        self.assertEqual(wrapped_coords_3, (1, 3))
    
    def test_conversion(self) -> None:
        converted_index = self.grid.to_index(1, 2)
        converted_coords = self.grid.to_coordinates(6)

        self.assertEqual(converted_index, 6)
        self.assertEqual(converted_coords, (1, 2))
    
    def test_iteration(self) -> None:
        elems = [e for e in self.grid]
        self.assertEqual(elems, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'])
    
    def test_proximity_iteration(self) -> None:
        it1 = self.grid.proximity_iterator(0, 0)
        exp1 = {'b', 'e', 'f'}

        it2 = self.grid.proximity_iterator(2, 1)
        exp2 = {'i', 'e', 'f', 'g', 'k'}

        it3 = self.grid.proximity_iterator(1, 2)
        exp3 = {'b', 'c', 'd', 'f', 'h', 'j', 'k', 'l'}

        self.assertEqual(exp1, {e for e in it1})
        self.assertEqual(exp2, {e for e in it2})
        self.assertEqual(exp3, {e for e in it3})
    
    def test_wrap_index_exception(self) -> None:
        with self.assertRaises(IndexError):
            self.grid.wrap_index(-13)
        with self.assertRaises(IndexError):
            self.grid.wrap_index(12)

    def test_wrap_coords_exception(self) -> None:
        with self.assertRaises(IndexError):
            self.grid.wrap_coordinates(-4, -5)
        
        with self.assertRaises(IndexError):
            self.grid.wrap_coordinates(3, 4)
        
        with self.assertRaises(IndexError):
            self.grid.wrap_coordinates(-6, 2)
        
        with self.assertRaises(IndexError):
            self.grid.wrap_coordinates(6, 1)

if __name__ == '__main__':
    unittest.main()