import tkinter, tkinter.messagebox, tkinter.simpledialog
import os
import sys

sys.path.append(os.path.dirname(__file__).replace('gui', ''))

from datetime import datetime
from minesweeper import Minesweeper
from minesweeper import CellState
from minesweeper import GameState
try:

  class Grid(Minesweeper):
    def __init__(self):
      super().__init__()
      self.minesweeper = Minesweeper()
      self.screen = tkinter.Tk()
      self.buttons = [[None for row in range(self.SIZE)] for column in range(self.SIZE)]

    def make_board(self):
      self.screen.title("Minesweeper")
      self.minesweeper.set_mines(datetime.now())

    def set_buttons(self):
      for row in range(0, 10):
        for column in range(0, 10):
          button = tkinter.Button(self.screen, height=2, width=6)
          button.bind("<Button-1>", lambda e, row=row, column=column: self.left_click_button(row, column))
          button.bind("<Button-2>", lambda e, row=row, column=column: self.right_click_button(row, column))
          button.bind("<Button-3>", lambda e, row=row, column=column: self.right_click_button(row, column))
          button.grid(row=row+1, column=column, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
          self.buttons[row][column] = button

    def left_click_button(self, row, column):
      self.minesweeper.expose_cell(row, column)
      if self.minesweeper.is_game_lost():
        self.show_all_mines()
        tkinter.messagebox.showinfo("YOU LOSE", "BOOM! You have exposed a mine.")
      else:
        self.update_exposed_cells()
        if self.minesweeper.get_game_status() == GameState.WON:
          tkinter.messagebox.showinfo("YOU WIN", "You are a master of minesweeper.")

    def right_click_button(self, row, column):
      self.minesweeper.toggle_seal(row, column)
      if self.minesweeper.get_cell_state(row, column) == CellState.SEALED:
        self.buttons[row][column].config(text="?")
      else:
        self.buttons[row][column].config(text="")

    def show_exposed_cells(self, row, column, exposure, adjacent):
      if exposure == CellState.EXPOSED:
        self.buttons[row][column].config(background="white")
      if adjacent != 0 and exposure == CellState.EXPOSED:
        self.buttons[row][column].config(text=str(adjacent))

    def update_exposed_cells(self):
      for row in range(0, 10):
        for column in range(0, 10):
          exposure = self.minesweeper.cellStates[row][column]
          adjacent = self.minesweeper.adjacent_mines_count_at(row, column)
          self.show_exposed_cells(row, column, exposure, adjacent)

    def show_all_mines(self):
      for row in range(0, 10):
        for column in range(0, 10):
          if self.minesweeper.mines[row][column]:
            self.buttons[row][column].config(background="red", text="*")

  newGame = Grid()
  newGame.make_board()
  newGame.set_buttons()
  newGame.screen.mainloop()
except:
  print("Ran on Jenkins")