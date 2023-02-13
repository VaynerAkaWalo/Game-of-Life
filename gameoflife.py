import copy
import os
import time
import random


# Klasa pomocnicza oddziela silnik gry od manipulacji planszą
class Board:

    def __init__(self, x, y) -> None:
        # Szerokość planszy
        self.col = x
        # Wysokość planszy
        self.rows = y
        # Znak wypisywany jako martwa komórka
        self.deadcharacter = '0'
        # Znak wypisywany jako żywa komórka
        self.alivecharacter = 'X'
        # Inicjalizacja planszy jako tablicy dwu-wymiarowej
        self.board = [['0' for _ in range(x)] for _ in range(y)]

    def __str__(self) -> str:
        # Złączenie całej tablicy w jeden string.
        # Żywe komórki wyświetlane są jako zielone, martwe jako białe.
        # Tło ustawione jest na czarne
        return "\n".join(" ".join("\033[1;37;37m " #37
                                  + self.deadcharacter
                                  if x == '0' else "\033[1;32;32m " #32
                                                   + self.alivecharacter
                                  for x in y) for y in self.board)

    # Możliwość zmiany znaku, który będzie wyświetlany jako martwa komórka.
    # Zmiana jest tylko kosmetyczna, nie zmienia znaków zapisywanych w tablicy.
    def changedeadcharacter(self, char):
        if not type(char) == str or len(char) > 1:
            raise ValueError("Parametr nie jest znakiem")
        self.deadcharacter = char

    # Możliwość zmiany znaku, który będzie wyświetlany jako żywa komórka.
    # Zmiana jest tylko kosmetyczna, nie zmienia znaków zapisywanych w tablicy.
    def changealivecharacter(self, char):
        if not type(char) == str or len(char) > 1:
            raise ValueError("Parametr nie jest znakiem")
        self.alivecharacter = char

    # Funkcja, która wypełnia planszę tak, aby na planszy była wskazana ilości
    # żywych komórek.
    def fillBoard(self, lifecells):
        if lifecells < 0:
            raise ValueError("Ilość komórek nie może byc ujemna")
        if lifecells > self.col * self.rows:
            raise ValueError("Tyle komórek nie zmieści się na planszy")

        # Sprawdzamy ile jest aktualnie żywych komórek
        counter = 0
        for x in range(self.col):
            for y in range(self.rows):
                if self.board[y][x] == 'X':
                    counter += 1

        lifecells -= counter

        # Ożywiamy komórki na losowych koordynatach tak długo aż będzie wskazana
        # liczba żywych komórek
        while lifecells > 0:
            x = random.randint(0, self.col - 1)
            y = random.randint(0, self.rows - 1)
            if self.board[y][x] == '0':
                self.board[y][x] = 'X'
                lifecells -= 1

    # Funkcja, która sprawdza, czy na tablicy zmieści się obiekt,
    # którego lewy góry róg leży w koordynatach x, y
    # i ma określoną wysokość i szerokość.
    def checkforspace(self, x, y, height, width):
        if x < 0 or y < 0 or x >= width or y >= height:
            raise ValueError("pozycja[y][x] nie należy do tablicy")
        if height < 1 or width < 1:
            raise ValueError("Wysokośc i szerokośc nie może być mniejsza "
                             "od jeden")

        return x + height < self.col and y + width < self.rows

    # Funkcja pozwala na ustawienie komórki o podanych koordynatach jako żywą
    def setasalive(self, x, y):
        if x < 0 or x >= self.col:
            raise ValueError("Pozycja X nie należy do tablicy")
        if y < 0 or y >= self.rows:
            raise ValueError("Pozycja Y nie należy do tablicy")

        self.board[y][x] = "X"


# Klasa implementująca silnik Game of Life
class GameOfLife:

    def __init__(self, board) -> None:
        if not isinstance(board, Board):
            raise ValueError("Proszę podać poprawny obiekt klasy Board")
        self.board = board
        self.height = board.rows
        self.width = board.col
        # Minimalna liczba sąsiadów, aby komórka przeżyła
        self.mintosurvive = 2
        # Maksymalna liczba sąsiadów, aby komórka przeżyła
        self.maxtosurvive = 3
        # Minimalna liczba sąsiadów, aby komórka się urodziła
        self.mintoborn = 3
        # Maksymalna liczba sąsiadów, aby komórka się urodziła
        self.maxtoborn = 3

    def __str__(self) -> str:
        return self.board.__str__()

    # Możliwość zmiany standardowych zasad gry.
    def changegamerules(self, mintosurvive, maxtosurvive, mintoborn, maxtoborn):
        if mintosurvive < 0 or maxtosurvive < 0 \
                or mintoborn < 0 or maxtoborn < 0:
            raise ValueError("Argumenty nie mogą być mniejsze od zera")
        if mintosurvive > maxtosurvive:
            raise ValueError("mintosurvive nie może " 
                             "być mniejszy od maxtosurvive")
        if mintoborn > maxtoborn:
            raise ValueError("mintoborn nie może być mniejszy od maxtoborn")
        self.maxtoborn = maxtoborn
        self.mintoborn = mintoborn
        self.maxtosurvive = maxtosurvive
        self.mintosurvive = mintosurvive

    # Funkcja obliczająca ilość sąsiadów danej komórki.
    # Jako sąsiadów rozumiemy komórki o indeksach x+-1
    # oraz y+-1 od naszej komórki
    def neighbours(self, x, y):
        # Komórka może leżeć na brzegu i wtedy nie można
        # sprawdzać indeksów poza tablicą
        minx = max(x - 1, 0)
        maxx = min(self.width, x + 2)
        miny = max(y - 1, 0)
        maxy = min(self.height, y + 2)

        counter = 0
        for i in range(minx, maxx, 1):
            for j in range(miny, maxy, 1):
                if not i == x or not j == y:
                    if self.board.board[j][i] == "X":
                        counter += 1
        return counter

    # Funkcja zmieniająca stan planszy o pojedynczą iterację
    def step(self):
        # Kopia oryginalnej tablicy, ponieważ stan komórek w
        # następnej iteracji musi zależeć od stanu w poprzedniej iteracji ->
        # zmiana stanu wszystkich komórek musi następować w tym samym czasie.
        tempboard = copy.deepcopy(self.board.board)
        for x in range(self.width):
            for y in range(self.height):
                # Obliczamy ilość sąsiadów danej komórki.
                numberofneighbours = self.neighbours(x, y)
                # Zmieniamy stan danej komórki w następnej iteracji zależnie
                # od ilości sąsiadów oraz aktualnych zasad gry.
                if self.board.board[y][x] == "X":
                    if numberofneighbours > self.maxtosurvive \
                            or numberofneighbours < self.mintosurvive:
                        tempboard[y][x] = '0'
                else:
                    if self.mintoborn <= numberofneighbours <= self.maxtoborn:
                        tempboard[y][x] = 'X'

        self.board.board = tempboard


if __name__ == '__main__':
    board = Board(35, 25)
    board.fillBoard(500)
    game = GameOfLife(board)
    for i in range(100):
        game.step()
        os.system('cls||clear')
        print(game)
        time.sleep(1)
