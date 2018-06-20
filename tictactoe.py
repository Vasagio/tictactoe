from __future__ import print_function, division
from builtins import range, input
import numpy as np
import matplotlib.pyplot as plt


#Sztuczna inteligencja
class AI:
  def __init__(self, eps=0.1, alpha=0.2):
    self.eps = eps # Epsilon, prawdopodobieństwo wykonania losowego ruchu
    self.alpha = alpha #prędkość uczenia się (learning rate) - do wzoru Ballman Equation
    self.state_information = False
    self.state_history = []

  def setV(self, V): #Ustawienie stanu
    self.V = V

  def set_symbol(self, sym):  #Ustawienie symbolu (X lub O)
    self.sym = sym

  def set_state_information(self, v):
    # Wyświetl wartości dla każdej pozycji tablicy
    self.state_information = v

  def reset_history(self):
    self.state_history = []

  def take_action(self, env):
    # #Zagraj kolejny ruch, losowy, albo najlepszy możliwy
     #Losowy ruch, aby nie wpaść w maksimum lokalne, sztuczna inteligencja czasami robi losowy ruch aby odkryć kolejne pola
    random = np.random.rand()
    best_state = None
    if random < self.eps:
       #Losowy ruch

      possible_moves = []
      for i in range(3):
        for j in range(3):
          if env.is_empty(i, j):
            possible_moves.append((i, j))
      idx = np.random.choice(len(possible_moves))
      next_move = possible_moves[idx]
    else:
        #wybierz najlepszy ruch na podstawie wartości stanów
        # pobierz w pętli wszystkie możliwe ruchy (podwójna pętla)
      pos2value = {}
      next_move = None
      best_value = -1 #najlepsza możliwa wartość ("śledzimy ją" w pętli)
      for i in range(3):
        for j in range(3):
          if env.is_empty(i, j):

            env.board[i,j] = self.sym
            state = env.get_state()
            env.board[i,j] = 0 #
            pos2value[(i,j)] = self.V[state]
            if self.V[state] > best_value:
              best_value = self.V[state]
              best_state = state
              next_move = (i, j)

      # Wyświetlanie wartości stanów na konsole
      if self.state_information:

        for i in range(3):
          print("------------------")
          for j in range(3):
            if env.is_empty(i, j):
              # print the value
              print(" %.2f|" % pos2value[(i,j)], end="")
            else:
              print("  ", end="")
              if env.board[i,j] == env.x:
                print("X  |", end="")
              elif env.board[i,j] == env.o:
                print("O  |", end="")
              else:
                print("   |", end="")
          print("")
        print("------------------")

     # Następny ruch (next_move)
    env.board[next_move[0], next_move[1]] = self.sym

    #Aktualizujemy tablicę stanów
  def update_state_history(self, s):
    self.state_history.append(s)

  def update(self, env):
        # V(prev_state) = V(prev_state) + alpha*(V(next_state) - V(prev_state)) - Bellman Equation
    reward = env.reward(self.sym) #nagroda (reward)
    target = reward
    for prev in reversed(self.state_history):
      value = self.V[prev] + self.alpha*(target - self.V[prev]) #Bellman Equation
      self.V[prev] = value
      target = value
    self.reset_history()


#Środowisko gry (rysowanie tablicy, sprawdzanie zwycięzcy, stanów, kółko i krzyżyk)
class TicTacToe:
  def __init__(self): #Konstruktor
    self.board = np.zeros((3, 3)) #uzupełnienie dwuwymiarowej tablicy 3 na 3 zerami (czyli pusta tablica, 0 = puste)
    self.x = -1 # Wartość -1 dla X
    self.o = 1 # Wartość 1 dla O
    self.winner = None #Na początku nie ma zwycięzcy
    self.ended = False #Na początku gra nie jest skończona, czyli false
    self.num_states = 3**(3*3) #9 pól na tablicy (3*3) i 3 stany dla każdego pola (Kółko, krzyżyk, puste(0)), 3^9

  def is_empty(self, i, j): #Czy pole jest puste)
    return self.board[i,j] == 0

  def reward(self, sym): #Nagroda (reward) przyznawana dopiero po skończonej grze
    if not self.game_over():
      return 0

    return 1 if self.winner == sym else 0 #Jeśli X wygrał, przyznajemy mu nagrodę 1

    #odwzorowanie stanu dla konkretnego pola
    #trzy możliwe stany: puste(0), X (1) i O(2) dla każdego pola
    #każde z 9 pól możemy ustawić na 3 sposoby, stąd 3^9, tak jak w rachunku prawdopodobieństwa
  def get_state(self):
    # Zwraca aktualny stan
    k = 0  #aktualna lokalizacja, numer pola na planszy
    h = 0  #hash, wartość danego pola, 3 do potęgi k(numer pola), pomnożona przez wartość stanu V (kółko, krzyżyk, puste)
    for i in range(3):
      for j in range(3):
        if self.board[i,j] == 0:
          v = 0
        elif self.board[i,j] == self.x:
          v = 1
        elif self.board[i,j] == self.o:
          v = 2
        h += (3**k) * v
        k += 1
    return h

  def game_over(self, force_recalculate=False): #sprawdzamy czy gra się zakończyła, force_recalculate jeśli gra się zakończyła, nie chcemy znowu sprawdzać
    if not force_recalculate and self.ended:
      return self.ended


      #Sprawdzamy czy ktoś wygrał (w kolumnach, wierszach i po skos)

      #Sprawdzamy wiersze
    for i in range(3):
      for player in (self.x, self.o):
        if self.board[i].sum() == player*3:
          self.winner = player #Ustawiamy który gracz ewentualnie wygrał
          self.ended = True #Ustawiamy skończoną gre na true
          return True #True kiedy gra jest skończona (ktoś wygrał, albo jest remis)


    #Sprawdzamy w kolumnach
    for j in range(3):
      for player in (self.x, self.o):
        if self.board[:,j].sum() == player*3:
          self.winner = player
          self.ended = True
          return True

    # Sprawdzamy na skos
    for player in (self.x, self.o):
      # Lewy górny - prawy dolny
      if self.board.trace() == player*3:
        self.winner = player
        self.ended = True
        return True
      # Odwracamy tablicę i sprawdzamy prawy-górny - lewy-dolny
      if np.fliplr(self.board).trace() == player*3:
        self.winner = player
        self.ended = True
        return True

    # Sprawdź czy jest remis (wszystkie pola zapełnione, nikt nie wygrał)
    if np.all((self.board == 0) == False):
      self.winner = None  #Nie ma zwycięzcy (remis)
      self.ended = True #Ale gra się skończyła (ended = True)
      return True

    # Gra się jeszcze nie skończyła
    self.winner = None
    return False

    #Ustawiamy wartości dla remisu
  def is_draw(self):
    return self.ended and self.winner is None


    #Rysujemy tablice w konsoli
  def draw_board(self):
    for i in range(3):
      print("-------------")
      for j in range(3):
        print("  ", end="")
        if self.board[i,j] == self.x:
          print("X ", end="")
        elif self.board[i,j] == self.o:
          print("O ", end="")
        else:
          print("  ", end="")
      print("")
    print("-------------")


#Człowiek
class Human:
  def __init__(self): #Konstruktor
    pass

  def set_symbol(self, sym): #Symbol dla gracza-człowieka (O lub X)
    self.sym = sym

  def take_action(self, tictactoe): #Wykonanie ruchu
    while True:
        #pętla się wykonuje dopóki nie wykonamy poprawnego ruchu
      move = input("Podaj współrzędne x, y dla kolejnego ruchu (z przedziału 0-2, np 1,1): ") #Pobieramy współrzędne od gracza w konsoli
      i, j = move.split(',') #Dzielimy Stringi na dwie wartości (dwie współrzędne)
      #castujemy nasze stringi na inty, żeby "włożyć" je do tablicy
      i = int(i)
      j = int(j)
      if tictactoe.is_empty(i, j):
        tictactoe.board[i,j] = self.sym
        #break jeśli zrobiliśmy poprawny ruch
        break

  def update(self, tictactoe):
    pass

  def update_state_history(self, s):
    pass

#Funkcja rekurencyjna
#Sprawdza całą tablice
# Zwraca wszystkie możliwe stany

def get_state_winner(tictactoe, i=0, j=0):
  results = []

  for v in (0, tictactoe.x, tictactoe.o):
    tictactoe.board[i,j] = v #Jeśli tablica jest pusta, v = 0
    if j == 2:
      if i == 2:
        # i=2, j=2, tablica jest pełna
        state = tictactoe.get_state() #pobieramy stan
        ended = tictactoe.game_over(force_recalculate=True)
        winner = tictactoe.winner #zwycięzca
        results.append((state, winner, ended)) #dodajemy wartości (append)
      else:
          #Inkrementujemy i
        results += get_state_winner(tictactoe, i + 1, 0)
    else:
      # Inkrementujemy j
      results += get_state_winner(tictactoe, i, j + 1)

  return results


#Zwraca wartość stanu dla X
# Jeśli wygra X, V(s) = 1
# Jeśli X przegra, albo będzie remis, V(s) = 0
# Else V(s) = 0.5
def initialV_x(tictactoe, state_winner_triples):
  V = np.zeros(tictactoe.num_states)
  for state, winner, ended in state_winner_triples:
    if ended:
      if winner == tictactoe.x:
        v = 1
      else:
        v = 0
    else:
      v = 0.5
    V[state] = v
  return V


def initialV_o(tictactoe, state_winner_triples):
    #Analogicznie do poprzedniej funkcji
    #Zwraca wartość stanu dla O
    #Jeśli O wygra, V(S) = 1
    #Jeśli O przegra, albo będzie remis, V(s) = 0
    #Else V(s) = 0.5
  V = np.zeros(tictactoe.num_states) #Tablica, na początku inicjujemy ją z samymi zerami (np. zeros)
  for state, winner, ended in state_winner_triples:
    if ended:
      if winner == tictactoe.o:
        v = 1
      else:
        v = 0
    else:
      v = 0.5
    V[state] = v
  return V


#Zagraj
def play_game(player1, player2, tictactoe, draw=False):
  # Pętla while dopóki gra się nie skończy
  current_player = None
  while not tictactoe.game_over():
      #Player1 zaczyna (można by ustawić żeby losowy gracz zaczynał)
      #Zmieniamy ruchy dla kolejnych graczy
      #Jeśli grał player1 zmieniamy na gracza player2, i analogicznie w drugą stronę
    if current_player == player1:
      current_player = player2
    else:
      current_player = player1

    # wyświetl tablicę w konsoli zanim kolejny gracz zrobi ruch
    if draw:
      if draw == 1 and current_player == player1:
        tictactoe.draw_board()
      if draw == 2 and current_player == player2:
        tictactoe.draw_board()

    # aktualny gracz robi ruch (player1 albo player2)
    current_player.take_action(tictactoe)

    # aktualizujemy tablice stanów
    state = tictactoe.get_state()
    player1.update_state_history(state)
    player2.update_state_history(state)

    #rysujemy tablice
  if draw:
    tictactoe.draw_board()

 #aktualizujemy stany graczy
  player1.update(tictactoe)
  player2.update(tictactoe)

if __name__ == '__main__': #funkcja main

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
  while True:
    player1.set_state_information(True)
    play_game(player1, human, TicTacToe(), draw=2)
    answer = input("Czy chcesz zagrać ponownie? [Y/n]: ")
    if answer and answer.lower()[0] == 'n':
      break
