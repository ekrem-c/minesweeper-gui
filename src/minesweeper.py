from enum import Enum
import random

class CellState(Enum):
  UNEXPOSED = 1
  EXPOSED = 2
  SEALED = 3

class GameState(Enum):
  INPROGRESS = 1
  LOST = 2
  WON = 3

class Minesweeper:
  def __init__(self):
    self.SIZE = 10
    self.cellStates = [[CellState.UNEXPOSED for row in range(self.SIZE)] for column in range(self.SIZE)]
    self.mines = [[False for row in range(self.SIZE)] for column in range(self.SIZE)]

  def set_mine(self, row, column):
    self.mines[row][column] = True

  def set_mines(self, seed):
    random.seed(seed)
    count = 10
    while count > 0:
      row = random.randint(0, 9)
      column = random.randint(0, 9)
      count = count - (not self.mines[row][column])
      self.set_mine(row, column)

  def get_cell_state(self, row, column):
    return self.cellStates[row][column]

  def expose_cell(self, row, column):
    if self.cellStates[row][column] == CellState.UNEXPOSED:
      self.cellStates[row][column] = CellState.EXPOSED
      if self.adjacent_mines_count_at(row, column) == 0:
        self.expose_neighbors(row, column)

  def expose_neighbors(self, row, column):
    for i in range(max(row - 1, 0), min(row + 2, 10)):
      for j in range(max(column - 1, 0), min(column + 2, 10)):
        self.expose_cell(i, j)

  def toggle_seal(self, row, column):
    self.cellStates[row][column] = {
      CellState.UNEXPOSED: CellState.SEALED,
      CellState.SEALED: CellState.UNEXPOSED,
      CellState.EXPOSED: CellState.EXPOSED
    }[self.cellStates[row][column]]

  def is_game_lost(self):
    for row in range(0, 10):
      for column in range(0, 10):
        if self.cellStates[row][column] == CellState.EXPOSED and self.mines[row][column]:
          return True
    return False

  def get_game_status(self):
    if self.is_game_lost():
      return GameState.LOST
    if self.is_game_still_in_progress():
      return GameState.INPROGRESS
    return GameState.WON

  def is_game_still_in_progress(self):
    for row in range(0, 10):
      for column in range(0, 10):
        if self.cellStates[row][column] == CellState.UNEXPOSED and self.mines[row][column] is False:
          return True
    return False

  def is_mine_at(self, row, column):
    return row in range(0, 10) and column in range(0, 10) and self.mines[row][column]

  def adjacent_mines_count_at(self, row, column):
    adjacent_count = 0

    for i in range(max(row - 1, 0), min(row + 2, 10)):
      for j in range(max(column - 1, 0), min(column + 2, 10)):
        if self.mines[i][j]:
          adjacent_count += 1

    return adjacent_count - 1 if self.mines[row][column] else adjacent_count
