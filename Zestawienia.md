# instrukcja krok po kroku tworzenia zestawień na kilku przykładach

# Wstęp #

Instrukcja w oparciu o przykłady prezentuje sposób tworzenia zestawień w programie QAZP2 i przestrzennej bazie danych. Przed przystąpieniem do tworzenia zestawień należy uruchomić edytor wybierają z menu **Zestawienia** opcję **Utwórz nowe zestawienie**.

# Zestawienie jednostek kulturowych bez warunków #

Zestawienie określi liczbę stanowisk w bazie danych z podziałem na obszar AZP oraz jednostkę kulturową.

1. Po uruchomieniu edytora widoczna jest pusta tabela z jednym wierszem i trzema kolumnami: (1) _Funkcja_ , (2) _Grupowanie_ i (3) _Warunek ORAZ_.

2. W kolumnie (1) wybierz funkcję agregującą _LICZ()_, która obliczy, ile wierszy należy do wyznaczonych grup.

3. W kolumnie (2) w pierwszym wierszu wybierz pole _Stanowisko.Obszar AZP_. Oznacza to, że wszystkie stanowiska zostaną podzielone według numeru arkusza. Na przykład jeżeli w bazie znajdują się stanowiska z 5 arkuszy, to na zestawieniu znajdzie się 5 wierszy i dla każdego z nich będzie określona liczba stanowisk, które znajdują się na danym obszarze.

4. W kolumnie (2), w drugim wierszu wybierz pole _Jednostka.Nazwa_. Oznacza to, że po pierwszym podziale stanowiska na każdym arkuszu zostaną dodatkowo rozdzielone według jednostki kulturowej, z którymi są związane.

5. Po tym kroku tabela edytora będzie wyglądała następująco
| **Funkcja** | **Grupowanie** | **Warunek ORAZ** |
|:------------|:---------------|:-----------------|
| LICZ() | Stanowisko.Obszar AZP |  |
|  | Jednostka.Nazwa |  |

# Zestawienie jednostek kulturowych z warunkami #

Aby ograniczyć stanowiska tylko do tych, których wartość określono jako (średnią ALBO dużą) ORAZ jako zagrożone, w edytorze zestawień należy dodać odpowiednie warunki.

1. Wykonaj czynności opisane w poprzednim paragrafie **Zestawienie jednostek kulturowych bez warunków**.


2. W kolumnie (3), w pierwszym wierszu wybierz pole _Wnioski.Wartosc_. Oznacza to, że po zakończeniu projektowania zestawienia zostanie wyświetlona prośba, czy mają być wyszukane stanowiska o małej wartości poznawczej, czy o średniej, czy o dużej. Tego wyboru dokonuje użytkownik.


3. Po tym kroku tabela edytora wygląda następująco:
| **Funkcja** | **Grupowanie** | **Warunek ORAZ** | **Warunek LUB** |
|:------------|:---------------|:-----------------|:----------------|
| LICZ() | Stanowisko.Obszar AZP | Wnioski.Wartosc |  |
|  | Jednostka.Nazwa |  |


4. W nowej kolumnie (4), która ma tytuł _Warunek LUB_, w pierwszym wierszu wybierz pole _Wnioski.Wartosc_. Kiedy program będzie tworzył zestawienie dwa razy zapyta użytkownika o parametr Wnioski.Wartosc i pobierze wszystkie stanowiska, które w tym polu mają informację równą jednej z wprowadzonych przez użytkownika. Na przykład jeżeli użytkownik w pierwszym parametrze poda wartość "Duża", a w drugi wartość "Średnia", to zostaną pobrane **wszystkie stanowiska, których wartość jest duża**<font color='red'>LUB</font> średnia**.**


5. Po tym kroku tabela edytora wygląda następująco:
| **Funkcja** | **Grupowanie** | **Warunek ORAZ** | Warunek LUB|Warunek LUB|
|:------------|:---------------|:-----------------|:-----------|:----------|
| LICZ() | Stanowisko.Obszar AZP | Wnioski.Wartosc | Wnioski.Wartosc |  |
|  | Jednostka.Nazwa |  |  |


6. W kolumnie (3), w drugim wierszu wybierz pole _Zagrozenia.Wystepowanie_, aby uzyskać następujący stan edytora:
| **Funkcja** | **Grupowanie** | **Warunek ORAZ** | Warunek LUB|Warunek LUB|
|:------------|:---------------|:-----------------|:-----------|:----------|
| LICZ() | Stanowisko.Obszar AZP | Wnioski.Wartosc | Wnioski.Wartosc |  |
|  | Jednostka.Nazwa | Zagrozenia.Wystepowanie |  |


7. Przed rozpoczęciem tworzenia zestawienia program zapyta się dwa razy o parametr _Wnioski.Wartosc_ i o parametr _Zagrozenia.Występowanie_. Na przykład jeżeli użytkownik w pierwszym parametrze _Wnioski.Wartość_ poda "Duża", w drugim parametrze _Wnioski.Wartość_ poda "Średnia", a w parametrze _Zagrozenia.Wystepowanie_ wybierze opcję "Istnieje", to pod uwagę zostaną wzięte **wszystkie stanowiska, których ( wartość jest duża**<font color='red'>LUB</font> średnia ) <font color='red'>ORAZ</font> są zagrożone