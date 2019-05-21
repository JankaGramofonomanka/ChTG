Ten program jest napisany w języku python3.7, 
aby go uruchomić trzeba mieć zaintsalony python:

https://www.python.org/downloads/

oraz bibliotekę matplotlib,
aby zainstalować matplotlib otwórz wiersz poleceń i wpisz następujące 
polecenie:

>> pip install matplotlib

Aby uruchomić program przejdź do folderu z programem i uruchom plik main.py
można to zrobić wpisując w wierszu poleceń:

>> python main.py


Obsługa programu:

Po uruchomieniu programu otworzy się okno z pustym wykresem, oraz przyciskami:

1) 'New Random Graph' - tworzy graf losowy i przedstawia go na wykresie,
2) 'DSatur' - koloruje stworzony wcześniej graf według algorytmu DSatur,
3) 'GIS' - koloruje stworzony wcześniej graf według algorytmu GIS,
4) 'GISbis' - koloruje stworzony wcześniej graf według algorytmu GISbis,
5) 'TURBOColor3000' - koloruje stworzony wcześniej graf według algorytmu 
	TURBOColor3000,
6) 'Change Colors' - zmienia kolory podstawiane pod liczby przypisane 
	wierzchołkom przez powyższe algorytmy
	(Kolory są dobierane losowo, więc zdarza się, że różne kolory są na 
	rysunku nieodróżnialne, wtedy należy nacisnąć przycisk 'Change Colors'.)

Użytkownik może również podać ilość wierzchołków grafu oraz wymiary 
powierzchni, na której mają być one losowane, służądo tego pola: 
'No. vertices', 'yrange' i 'xrange'.
Domyślna liczba wierzchołków to 100, domyślne wymiary to 10x10.


Opis algorytmów:

1) GISbis - działa prawie tak samo jak GIS, tylko przy wyznaczaniu zbioru 
	niezależnego, pierwszy wierzchołek to wierzchołek najbliższy punktu 
	(0, 0),
2) TURBOColor3000 - również działa na podstawie GIS, zbiór niezależny jest 
	wyznaczany następująco:

- znajdź wierzchołek v najbliżej punktu (0, 0)
- dla wszystkich wierzchołków w, takich że |v - w| < 1, wyznacz koła o 
	promieniu 0.5, takie, że ich brzeg przechodzi przez v i w
- wybierz z powyższych takie koło, które zawiera najwięcej wierzchołków i 
	dodaj je do zbioru niezależnego.
- usuń z grafu koło o promieniu 2.5 i środku tym samym, co wybrane wyżej koło
- powtórz czynność dla pozostałego grafu.