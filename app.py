from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import random
import numpy as np

from tictactoe import AI
from tictactoe import TicTacToe
from tictactoe import Human



class GridLayout(GridLayout):
    tablica = np.zeros((3,3))

    def take_action(self, choice):
        tablica = self.tablica

        i, j = choice.split(',')
        i = int (i)
        j = int (j)


        if tictactoe.is_empty(i, j):
          tictactoe.board[i,j] = self.sym




class TicTacToeApp(App):
    def build(self):
        return GridLayout()

if __name__ == "__main__":
    TicTacToeApp().run()
