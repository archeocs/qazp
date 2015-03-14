# Opis #

Wtyczka umożliwia import danych GPS do przestrzennej bazy SQL. Dane muszą być pobrane z odbiornika w formacie GPX (obsługiwanym przez większość urządzeń). Wtyczka zapisuje dane przestrzenne z dodatkowymi informacjami o autorze i opisem w tabeli bazy AZP2.


# Instrukcja #
  1. Nawiąż połączenie z przestrzenną bazą PostGIS / Spatialite.
![http://wiki.qazp.googlecode.com/hg/imgs/spatial.png](http://wiki.qazp.googlecode.com/hg/imgs/spatial.png) i wybierz warstwę **trasy**.
  1. Upewnij się, że warstwa jest zaznaczona jako aktywna (kliknij na niej).
  1. Z menu Plugins->AZP2-GPS wybierz **Importuj plik GPX**.
  1. W nowym oknie kliknij przycisk **Dodaj trasę** aby dodać trasę zapisaną w pliku GPX.
![http://wiki.qazp.googlecode.com/hg/imgs/glowne.png](http://wiki.qazp.googlecode.com/hg/imgs/glowne.png)
  1. Wskaż plik z rozszerzeniem GPX.
![http://wiki.qazp.googlecode.com/hg/imgs/wybor_gpx.png](http://wiki.qazp.googlecode.com/hg/imgs/wybor_gpx.png)
i potwierdź przyciskiem OK.
  1. W nowym oknie zostają wyświetlone wszystkie trasy znalezione we wskazanym pliku GPX, tak jak pokazano na rysunku poniżej.
![http://wiki.qazp.googlecode.com/hg/imgs/fragmenty.png](http://wiki.qazp.googlecode.com/hg/imgs/fragmenty.png)
    * Domyślnie zaznaczone są wszystkie trasy. Program scali je automatycznie w jedną ciągłą linię. Aby pominąć pewne trasy wystarczy odznaczyć je w tabeli.
    * Zwróć uwagę na wartość w polu **Współczynnik zmienności**. Jeśli rozpoczyna się od _Niski (Dobrze)_ to oznacza, że prawdopodobnie trasy rejestrowano w niewielkich odstępach czasu. W przeciwnym razie w tym polu będzie pisało _Wysoki (Źle)_. Wtedy należy przejrzeć czasy rozpoczęcia i zakończenia tras i w razie potrzeby wyeliminować te, które są nieprawidłowe.
  1. Wprowadź dodatkowe informacje o nowej trasie.
  1. Kliknij OK.

**Uwaga! Wtyczka nie sprawdza, czy w bazie danych są już informacje, które próbuje zapisać użytkownik**