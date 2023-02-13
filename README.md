# Game-of-Life


### Pythonowa implementacja silnika [Gry w życie](https://pl.wikipedia.org/wiki/Gra_w_życie)

W celach demonstracyjnych można bezpośrednio uruchomić plik gameoflife.py:
```
python gameoflife.py
```
Spowoduje to utworzenie planszy 35x25 oraz wypełnienie ją 500 żywymi komórkami,
a następnie w 1 sekundowych odstępach czasu zostanie wyświetlone następne 100 
iteracji gry w życie.

Żywe komórki wyświetlane są jako znak ```X``` - kolor zielony

Martwe komórki wyświetlane są jako znak ```0``` - kolor biały

## Dokumentacja

### Klasa ```Board``` służy do utworzenia, a następnie do manipulacji planszą.

Konstruktor klasy Board przyjmuje 2 parametry szerokość oraz wysokość planszy
```
Board(szerokość, długość)
```

Aby wyświetlić planszę należy do funkcji print podać obiekt klasy Board:
```
print(board)
```

Standardowo komórki martwe oraz żywe będą reprezentowane jako znaki '0' oraz 'X'
istnieje możliwość zmiany obu znaków przy użyciu funkcji wywołanych na 
obiekcie klasy Board:
```
board.changedeadcharacter(znak)
```
```
board.changealivecharacter(znak)
```

Do wypełnienia planszy żywymi komórkami można użyć funkcji ```fillboard```. 
Funkcja sprawdza ile jest aktualnie żywych komórek na planszy i w razie potrzeby
losuje miejsca dla nowych żywych komórek tak aby na planszy było tyle żywych
komórek ile zostało podanych w argumencie funkcji
```
board.fillboard(liczba żywych komórek)
```

Plansza pozwala również na manulane ustawianie które komórki są żywe, służy
do tego funkcja:
```
board.setasalive(x, y)
```

Jeżeli chcemy wprowadzić na plansze jakąś większą strukture możemy sprawdzić
czy zmieści się ona na ustalonych przez nas koordynatach służy do tego funkcja:
```checkforspace``` podajemy do niej koordynaty lewego górnego rogu 
oraz szerokość i wysokość naszej struktury.
```
board.checkforspace(x, y, height, width)
```

### Klasa ```GameOfLife``` implementuje silnik gry w życie.

Konstruktor klasy ```GameOfLife``` przyjmuje jako parametr 
plansze - obiekt klasy Board
```
GameOfLife(board)
```

Aby wypisać stan planszy przekazujemy obiekt klasy ```GameOfLife```:
```
print(gameoflife)
```

Jest możliwość zmiany standardowych zasad gry, służy do tego 
funkcja ```changegamerules``` do której przekazujemy nowe zasady
```
gameoflife.changegamerules(mintosurvive, maxtosurvive, mintoborn, maxtoborn)
```

Do wykonania pojedynczej iteracji gry w życie używamy funkcji:
```
gameoflife.step()
```