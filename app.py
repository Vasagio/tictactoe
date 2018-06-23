from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import random
import numpy as np

class GridLayout(GridLayout):
    tablica = np.zeros((3,3))

    def choice(self, choice):
        tablica = self.tablica
        i, j = choice.split(',')
        i = int (i)
        j = int (j)

        tablica[i,j] = -1
        print (tablica)



class TicTacToeApp(App):
    def build(self):
        return GridLayout()

if __name__ == "__main__":
    TicTacToeApp().run()
