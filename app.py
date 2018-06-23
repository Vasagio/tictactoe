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
  print("Loading...")
   #Konsola wyświetla informacje o ładowaniu podczas gdy zaraz dwie sztuczne inteligencje
   # będą grały ze sobą, co może chwilę potrwać jeśli ustawimy dużą ilość gier

  # Dwóch graczy (sztuczne inteligencje) grają między sobą i uczą się (inicjujemy dwóch graczy AI)
  player1 = AI()
  player2 = AI()

    #inicjujemy środowisko w którym będziemy grać

  tictactoe = TicTacToe()
  state_winner_triples = get_state_winner(tictactoe)

  # Ustawiamy wartości stanów dla graczy

  Vx = initialV_x(tictactoe, state_winner_triples)
  player1.setV(Vx)
  Vo = initialV_o(tictactoe, state_winner_triples)
  player2.setV(Vo)

  # give each player their symbol
  player1.set_symbol(tictactoe.x)
  player2.set_symbol(tictactoe.o)

  number_of_training_games = 5000 #liczba gier treningowych w których dwie sztuczne inteligencje grają ze sobą
  # można by to zainicjować z konsoli jako input, ale my już to ustawiliśmy "z palca"
  for n in range(number_of_training_games):
    play_game(player1, player2, TicTacToe())

    #gdy się już nasz AI wyszkolił, gramy Człowiek kontra Sztuczna inteligencja ;)
  human = Human()
  human.set_symbol(tictactoe.o)
  TicTacToeApp().run()
