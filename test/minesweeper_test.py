import unittest

from src.minesweeper import CellState
from src.minesweeper import GameState
from src.minesweeper import Minesweeper

class MinesweeperTests(unittest.TestCase):
  def setUp(self):
    self.minesweeper = Minesweeper()

  def test_Canary(self):
    self.assertTrue(True)

  def test_initially_cells_not_exposed(self):
    self.assertEqual(CellState.UNEXPOSED, self.minesweeper.get_cell_state(2, 3))

  def test_expose_unexposed_cell(self):
    self.minesweeper.expose_cell(1, 3)

    self.assertEqual(CellState.EXPOSED, self.minesweeper.get_cell_state(1, 3))

  def test_expose_an_exposed_cell(self):
    self.minesweeper.expose_cell(2, 4)

    self.minesweeper.expose_cell(2, 4)

    self.assertEqual(CellState.EXPOSED, self.minesweeper.get_cell_state(2, 4))


  def test_expose_an_out_of_bounds_cell(self):
    self.assertRaises(Exception, self.minesweeper.expose_cell, 11, 1)

  def test_seal_unexposed_cell(self):
    self.minesweeper.toggle_seal(1, 5)

    self.assertEqual(CellState.SEALED, self.minesweeper.get_cell_state(1, 5))

  def test_unseal_sealed_cell(self):
    self.minesweeper.toggle_seal(7, 7)

    self.minesweeper.toggle_seal(7, 7)

    self.assertEqual(CellState.UNEXPOSED, self.minesweeper.get_cell_state(7, 7))

  def test_seal_exposed_cell(self):
    self.minesweeper.expose_cell(5, 6)

    self.minesweeper.toggle_seal(5, 6)

    self.assertEqual(CellState.EXPOSED, self.minesweeper.get_cell_state(5, 6))

  def test_expose_sealed_cell(self):
    self.minesweeper.toggle_seal(3, 5)

    self.minesweeper.expose_cell(3, 5)

    self.assertEqual(CellState.SEALED, self.minesweeper.get_cell_state(3, 5))

  def test_expose_cell_calls_expose_neighbors(self):
    class MinesweeperWithExposeNeighborsStubbed(Minesweeper):
      self.called = False
      def expose_neighbors(self, row, column):
        self.called = True

    minesweeper = MinesweeperWithExposeNeighborsStubbed()

    minesweeper.expose_cell(2, 3)

    self.assertTrue(minesweeper.called)

  def test_already_exposed_no_call_expose_neighbor(self):
    class MinesweeperWithExposeNeighborsStubbed(Minesweeper):
      called = False
      def expose_neighbors(self, row, column):
        self.called = True

    minesweeper = MinesweeperWithExposeNeighborsStubbed()

    minesweeper.expose_cell(1, 5)
    minesweeper.called = False

    minesweeper.expose_cell(1, 5)

    self.assertFalse(minesweeper.called)

  def test_sealed_no_call_exposeneighbor(self):
    class MinesweeperWithExposeNeighborsStubbed(Minesweeper):
      called = False

      def expose_neighbors(self, row, column):
        self.called = True

    minesweeper = MinesweeperWithExposeNeighborsStubbed()

    minesweeper.toggle_seal(1, 5)
    minesweeper.expose_cell(1, 5)

    self.assertFalse(minesweeper.called)

  def test_exposeneighbor_calls_eight_neighbors(self):
    class MinesweeperWithExposeNeighborsStubbed(Minesweeper):
      called_locations = []
      def expose_cell(self, row, column):
        self.called_locations.append([row, column])

    prediction = [[4, 4], [4, 5], [4, 6], [5, 4], [5, 5], [5, 6], [6, 4], [6, 5], [6, 6]]
    minesweeper = MinesweeperWithExposeNeighborsStubbed()

    minesweeper.expose_neighbors(5, 5)

    self.assertEqual(prediction, minesweeper.called_locations)


  def test_exposeneighbor_topleft_cells(self):
    class MinesweeperWithExposeNeighborsStubbed(Minesweeper):
      called_locations = []
      def expose_cell(self, row, column):
        self.called_locations.append([row, column])

    prediction = [[0, 0], [0, 1], [1, 0], [1, 1]]
    minesweeper = MinesweeperWithExposeNeighborsStubbed()

    minesweeper.expose_neighbors(0, 0)

    self.assertEqual(prediction, minesweeper.called_locations)

  def test_exposeneighbor_bottomright_cells(self):
    class MinesweeperWithExposeNeighborsStubbed(Minesweeper):
      called_locations = []

      def expose_cell(self, row, column):
        self.called_locations.append([row, column])

    prediction = [[8, 8], [8, 9], [9, 8], [9, 9]]
    minesweeper = MinesweeperWithExposeNeighborsStubbed()

    minesweeper.expose_neighbors(9, 9)

    self.assertEqual(prediction, minesweeper.called_locations)

  def test_mines_initially_false(self):
    self.assertFalse(self.minesweeper.is_mine_at(3, 2))

  def test_set_mine(self):
    self.minesweeper.set_mine(3, 2)

    self.assertEqual(True, self.minesweeper.is_mine_at(3, 2))

  def test_set_mine_row_lower_bound(self):
    self.assertFalse(self.minesweeper.is_mine_at(-1, 4))

  def test_set_mine_row_upper_bound(self):
    self.assertFalse(self.minesweeper.is_mine_at(10, 5))

  def test_set_mine_column_lower_bound(self):
    self.assertFalse(self.minesweeper.is_mine_at(5, -1))

  def test_set_mine_column_upper_bound(self):
    self.assertFalse(self.minesweeper.is_mine_at(7, 10))

  def test_expose_cell_on_adjacent_cell_does_not_call_expose_neighbors(self):
    class MinesweeperWithExposeNeighborsStubbed(Minesweeper):
      called_locations = []

      def expose_cell(self, row, column):
        self.called_locations.append([row, column])

    minesweeper = MinesweeperWithExposeNeighborsStubbed()

    minesweeper.set_mine(3, 6)

    minesweeper.expose_cell(2, 6)

    prediction = [[2, 6]]

    self.assertEqual(prediction, minesweeper.called_locations)

  def test_expose_cell_adjacent_cell_expose_neighbors(self):
    self.minesweeper.set_mine(3, 6)

    self.minesweeper.expose_cell(2, 6)

    self.assertEqual(CellState.UNEXPOSED, self.minesweeper.get_cell_state(2, 7))

  def test_adjacent_cells_count_on_mine_is_zero(self):
    self.minesweeper.set_mine(3, 4)

    self.assertEqual(0, self.minesweeper.adjacent_mines_count_at(3, 4))

  def test_adjacent_cells_count_successfully_increment(self):
    self.minesweeper.set_mine(3, 4)

    self.assertEqual(1, self.minesweeper.adjacent_mines_count_at(3, 5))

  def test_multiple_mines_adjacent(self):
    self.minesweeper.set_mine(3, 4)

    self.minesweeper.set_mine(2, 6)

    self.assertEqual(2, self.minesweeper.adjacent_mines_count_at(3, 5))

  def test_adjacent_mine_count_upper_left_bound(self):
    self.minesweeper.set_mine(0, 1)

    self.assertEqual(1, self.minesweeper.adjacent_mines_count_at(0, 0))

  def test_adjacent_mine_count_upper_right_bound(self):
    self.assertEqual(0, self.minesweeper.adjacent_mines_count_at(0, 9))

  def test_adjacent_mine_count_lower_right_bound(self):
    self.minesweeper.set_mine(9, 8)

    self.assertEqual(1, self.minesweeper.adjacent_mines_count_at(9, 9))

  def test_adjacent_mine_count_lower_left_bound(self):
    self.assertEqual(0, self.minesweeper.adjacent_mines_count_at(0, 9))

  def test_game_status_initially_inprogress(self):
    self.assertEqual(GameState.INPROGRESS, self.minesweeper.get_game_status())

  def test_expose_mine_loses_game(self):
    self.minesweeper.set_mine(6, 1)

    self.minesweeper.expose_cell(6, 1)

    self.assertEqual(GameState.LOST, self.minesweeper.get_game_status())

  def test_inprogress_mines_sealed_cells_unexposed(self):
    self.temp = Minesweeper()

    self.temp.set_mine(5, 5)

    self.temp.toggle_seal(5, 5)

    self.assertEqual(GameState.INPROGRESS, self.temp.get_game_status())

  def test_inprogress_mines_sealed_cells_sealed(self):
    self.temp = Minesweeper()

    self.temp.set_mine(5, 5)

    self.temp.toggle_seal(5, 5)

    self.temp.toggle_seal(8, 8)

    self.assertEqual(GameState.INPROGRESS, self.temp.get_game_status())

  def test_inprogress_mines_sealed_adjacent_cell_unexposed(self):
    self.temp = Minesweeper()

    self.temp.set_mine(5, 5)

    self.temp.toggle_seal(5, 5)

    self.temp.toggle_seal(5, 5)

    self.assertEqual(GameState.INPROGRESS, self.temp.get_game_status())

  def test_won_mines_sealed_cells_exposed(self):
    self.temp = Minesweeper()

    self.temp.set_mine(9, 9)

    self.temp.toggle_seal(9, 9)

    self.temp.expose_cell(0, 0)

    self.assertEqual(GameState.WON, self.temp.get_game_status())

  def test_set_10_mines(self):
    self.minesweeper.set_mines(0)

    count = 0
    for row in range(10):
        for column in range(10):
            if self.minesweeper.is_mine_at(row, column) == True:
                count += 1

    self.assertEqual(10, count)


  def test_set_10_mines_with_different_seed(self):
    minesweeperSeed0 = Minesweeper()

    minesweeperSeed0.set_mines(0)

    minesweeperSeed1 = Minesweeper()

    minesweeperSeed1.set_mines(1)

    self.assertNotEqual(minesweeperSeed0.mines, minesweeperSeed1.mines)

  def test_exposeneighbor_border_cells(self):
    class MinesweeperWithExposeNeighborsStubbed(Minesweeper):
      called_locations = []

      def expose_cell(self, row, column):
        self.called_locations.append([row, column])

    prediction = [[8, 4], [8, 5], [8, 6], [9, 4], [9, 5], [9, 6]]
    minesweeper = MinesweeperWithExposeNeighborsStubbed()

    minesweeper.expose_neighbors(9, 5)

    self.assertEqual(prediction, minesweeper.called_locations)

if __name__ == '__main__':
    unittest.main()
