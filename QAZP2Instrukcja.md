#Instrukcja obsługi programu QAZP2



# Wstęp #

Program służy do zarządzania przestrzenną bazą danych z informacjami o stanowiskach archeologicznych, badaniach powierzchniowych i lotniczych we współpracy z programem QuantumGIS. W tej instrukcji opisane zostały najważniejsze funkcje bezpłatnego programu QAZP2, przy pomocy których można zarządzać informacjami o Archeologicznym Zdjęciu Polski.

Uzupełnieniem instrukcji jest seria filmów zamieszczonych na [kanale Youtube](http://www.youtube.com/channel/UCUkBtCronC8c8Y2mV2MXxyg/videos)

**Uwaga! Progam znajduje się w fazie intensywnego rozwoju i aktualizacje mogą powodować błędy**

# Instalacja #

Program jest instalowany za pośrednictwem repozytorium, którego definicja znajduje się w pliku [plugins.xml](http://qazp.googlecode.com/hg/plugins.xml). Instrukcja jest napisana przy pomocy anglojęzycznej wersji programu

## Dodawanie repozytorium w programie QuantumGIS ##
  1. Z menu **Plugins** wybierz **Fetch Python Plugins ...** ( **Plugins->Fetch Python Plugins** )
  1. Po aktualizacji listy wtyczek pojawi się nowe okno: **QGIS Python Plugin Installer**. Wybierz w nim zakładkę **Repositories**.
  1. Naciśnij przycisk **Add ...**.
  1. W nowym oknie wprowadź adres repozytorium: ` http://qazp.googlecode.com/hg/plugins.xml ` oraz nazwę, np. qazp-hg i naciśnij przycis **OK**. ![http://wiki.qazp.googlecode.com/hg/imgs/nowe_repo.png](http://wiki.qazp.googlecode.com/hg/imgs/nowe_repo.png)
  1. Po tej operacji zakładka **Repositories** powinna wyglądać tak jak pokazano na obrazku ![http://wiki.qazp.googlecode.com/hg/imgs/lista_repo.png](http://wiki.qazp.googlecode.com/hg/imgs/lista_repo.png)
  1. Przejdź do zakładki **Plugins** , wyszukaj program QAZP2 i naciśnij przycisk **Install Plugin** ![http://wiki.qazp.googlecode.com/hg/imgs/lista_plug.png](http://wiki.qazp.googlecode.com/hg/imgs/lista_plug.png)
  1. Po zainstalowaniu wtyczki naciśnij przycisk **Close**
  1. Z menu wybierz **Plugins->Manage Plugins**, wyszukaj QAZP2 i zaznacz tą wtyczkę. Od tej chwili w menu **Plugins** powinna być widoczna opcja QAZP

## Baza PostGIS ##
TBD

## Baza danych Spatialite ##
  1. Pobierz plik z pustą bazą danych http://qazp.googlecode.com/files/azp2_lite-0.11.zip i zapamiętaj katalog, w którym została zapisana.
  1. Rozpakuj pobrane archiwum.
  1. Z menu programu QuantumGIS wybierz **Layer->Add Spatialite Layer**.
  1. W nowym oknie kliknij przycisk **New** aby dodać bazę danych do listy. Ten krok trzeba wykonać tylko jeden raz, jeżeli bazy jeszcze nie ma na liście.
  1. Wskaż pobrany przed chwilą plik i zaakceptuj klikając przycisk **OK**. ![http://wiki.qazp.googlecode.com/hg/imgs/nowa_baza.png](http://wiki.qazp.googlecode.com/hg/imgs/nowa_baza.png)
  1. Z listy rozwijanej wybierz dodaną bazę danych i naciśnij przycisk **Connect**, aby wyświetlić listę warstw wektorowych, które są w niej zdefiniowane.
  1. Zaznacz warstwę **miejsca** i naciśnij przycisk **Add**. Aby dodać jeszcze warstwę **trasy** wykonaj ponownie krok 2, 4, 5.

![http://wiki.qazp.googlecode.com/hg/imgs/polaczenie.png](http://wiki.qazp.googlecode.com/hg/imgs/polaczenie.png)

# Import współrzędnych GPS miejsc #
  1. Jeżli QAZP2 jest zamknięte wybierając z menu **Plugins->QAZP2->QAZP2**.
  1. Na początku widoczne jest menu **Miejsca** i menu **Trasy** ![http://wiki.qazp.googlecode.com/hg/imgs/menu.png](http://wiki.qazp.googlecode.com/hg/imgs/menu.png)
  1. Z menu wybierz **Miejsca->Importuj z GPS**.
  1. Wskaż plik GPX, z którego mają być pobrane współrzędne i informacje z odbiornika GPS, a następnie naciśnij przycisk **OK** ![http://wiki.qazp.googlecode.com/hg/imgs/import_gps_open.png](http://wiki.qazp.googlecode.com/hg/imgs/import_gps_open.png)
  1. Jeżeli w pliku zosały znalezione punkty _waypoints_ zostaną one dodane do warstwy **miejsca** i zostanie wyświetlony stosowny komunikat po zakończeniu, który podaje liczbę dodanych punktów. ![http://wiki.qazp.googlecode.com/hg/imgs/import_gps_wynik_miej.png](http://wiki.qazp.googlecode.com/hg/imgs/import_gps_wynik_miej.png)

# Import współrzędnych GPS tras #
  1. Jeżli QAZP2 jest zamknięte wybierając z menu **Plugins->QAZP2->QAZP2**.
  1. Na początku widoczne jest menu **Miejsca** i menu **Trasy**.
  1. Z menu wybierz **Trasy->Importuj z GPS**.
  1. Wskaż plik GPX, z którego mają być pobrane współrzędne i informacje z odbiornika GPS, a następnie naciśnij przycisk **OK**.
  1. Jeżeli w pliku zosały znalezione segmenty (fragmenty) trasy _trk_, to ich lista zostanie wyświetlona w nowym oknie. ![http://wiki.qazp.googlecode.com/hg/imgs/import_trasy.png](http://wiki.qazp.googlecode.com/hg/imgs/import_trasy.png)
  1. Wypełnij informacje w taki sposób, jak pokazano na rysunku powyżej.
    1. Data pomiarów w formacie RRRR-MM-DD
    1. Autor - dane autora
    1. Rodzaj badań
    1. Częstotliwość odczytów - **średni** czas w sekundach między kolejnymi odczytami punktów, które składają się na trasę. Jest obliczany automatycznie, ale jest możliwa jego modyfikacja, jeżeli to konieczne.
    1. Współczynnik zmienności - wartość pokazuje, jak mocno czasy pomiarów odbiegają od średniej częstotliwości. Im jest ona bliższa zera tym lepiej. Jeżeli wartość jest wysoka - zbliżona do 1, to znaczy, że upłynęła znacząca ilość czasu pomiędzy rejestracją poszczególnych segmentów. Zmiany współczynnika można obserwować zaznaczając i odznaczając segmenty na liście
    1. Uwagi
  1. Po podaniu informacji wybierz segmenty, które mają być scalone w trasę (domyślnie wszystkie są zaznaczone) i kliknij **OK**, by zapisać nową trasę na warstwie **trasy**. Sukces operacji jest sygnalizowany komunikatem.

# Dodawanie stanowisk #
  1. Narysuj stanowisko na mapie
  1. W formularzu wprowadź informacje, które umożliwią później identyfikację stanowiska - obszar, nr na obszarze, itd. Pozostałe informacje o lokalizacji tj. miejscowośc, nr w miejscowości, gminę, powiat, województwo można określić edytując stanowiska

# Wyszukiwanie i edycja (na przykładzie warstwy miejsca) #
  1. Wybierz z menu **Miejsca->Wyszukaj** i podaj warunek wyszukiwania ![http://wiki.qazp.googlecode.com/hg/imgs/wyszukiwanie.png](http://wiki.qazp.googlecode.com/hg/imgs/wyszukiwanie.png)
  1. Wprowadź warunek, na przykład _nazwa='3B 027'_, który spowoduje wyświetlenie listy z punktami (w przykładzie jednym punktem), który w kolumnie nazwa ma wartość _3B 027_.
  1. Aby zmienić właściwości punktu, wybierz go na liście a następnie naciśnij przycisk **Zmień**. ![http://wiki.qazp.googlecode.com/hg/imgs/miejsca_lista.png](http://wiki.qazp.googlecode.com/hg/imgs/miejsca_lista.png)
  1. Właściwości miejsca są widoczne w postaci tabeli, gdzie w pierwszej kolumnie jest wpisana nazwa właściwości, np _Autor_, a w drugie jej wartość, np. _Anonim_ tak jak to przedstawia obrazek
> ![http://wiki.qazp.googlecode.com/hg/imgs/ed_miej.png](http://wiki.qazp.googlecode.com/hg/imgs/ed_miej.png)
  1. Aby zmienić wartość cechy należy wybrać odpowiednią komórkę i rozpocząć wpisywanie, albo kliknąć na niej dwa razy.
  1. Rodzaj badań wybiera się z listy rozwijanej.
  1. Wprowadzone zmiany są zapisywane po kliknięciu przycisku **Save**.
  1. Edytor miejsca można opuścić naciskając przycisk **Close**
  1. Lista punktów jest aktualizowana automatycznie.
  1. Aby wyświetlić wyszukane punkty jako nową warstwę naciśnij przycisk **Wyświetl**
  1. Zostaje dodana nowa warstwa z automaycznie nadaną nazwą, która zawiera tylko wybrane obiekty. ![http://wiki.qazp.googlecode.com/hg/imgs/mapa_miej.png](http://wiki.qazp.googlecode.com/hg/imgs/mapa_miej.png)

` Podpowiedź: Taką samą procedurę można zastosować do zmiany właściwości trasy `

# Wykazy lokalizacji #
  1. Do określenia lokalizacji konieczne jest utworzenie wykazów miejscowosci, gmin, powiatów i województ.
  1. Aby wyświetlić wykaz, z Menu **Wykazy** wybierz odpowiedni wykaz.
  1. Wykazy są wyświetlane w postaci tabeli z jedną kolumną, w której wypisane są wybrane w porządku alfabetycznym nazwy.  ![http://wiki.qazp.googlecode.com/hg/imgs/wykaz_nowa.png](http://wiki.qazp.googlecode.com/hg/imgs/wykaz_nowa.png)
  1. Poniżej tabeli znajduje się lista rozwijana, z której wybiera się nazwy, które mają być wyświetlane wskazują dwie pierwsze litery, od których się rozpoczynają. W przykładzie z obrazka powyżej wyświetlane są wszystkie miejscowości rozpoczynające się od liter _PO_
  1. W polu tekstowym obok pojawia się zaznaczona w tabeli nazwa.
  1. Aby dodać nową nazwę wpisz w polu tekstowym nazwę a następnie naciśnij przycisk **Dodaj**
  1. Aby zmienić nazwę, zaznacz ją w tabeli, w polu tekstowym zmień wartość a następnie kliknij przycisk **Zmień**
  1. Aby usunąć nazwę zaznacz ją w tabeli a następnie kliknij przycisk **Usuń**
  1. Edytor wykazów można opuścić naciskając przycisk **Zamknij**

# Wyświetlanie zaznaczony stanowisk #
Istnieje możliwość wyświetlania stanowisk, które są aktualnie zaznaczone w programie QGIS. Aby aktywować funkcję z menu **Stanowiska** należy wybrać opcję **Pokazuj zaznaczone**.

# Edycja stanowisk #
  1. Wyszukaj stanowiska według wybranych kryteriów.
  1. Wybierz stanowisko do zmiany i naciśnij przycisk **Edytuj**.
  1. Zostaje wyświetlony edytor do edycji miejsc. ![http://wiki.qazp.googlecode.com/hg/imgs/sted_przed.png](http://wiki.qazp.googlecode.com/hg/imgs/sted_przed.png)
  1. Jeżeli stanowisko nie ma określonej lokalizacji (położenia w obrębie miejscowości, gminy, itd.), to w odpowidnich wierszach pokazywana jest wartość _PUSTE_.
  1. Aby zmienić informacje o lokalizacji kliknij na odpowidnią komórkę dwa razy i z listy rozwijanej wybierz nazwę miejscowości, powiatu, gminy, albo województwa. Lista jest tworzona z nazw, które znajdują się w odpowiednim Wykazie.
  1. Właściwości stanowiska są podzielone na kategorie, których nazwy są wyświetlone po prawej stronie edytora w postaci przycisków.
  1. Po kliknięciu w jeden z przycisków jest wyświetlany edytor właściwości z odpowiedniej kategorii.
  1. W zależności od typu cechy jej wartość wybiera się z rozwijanej listy np Tak / Nie, Mały / Średni / Duży; albo wprowadza ręcznie jako liczbę lub tekst.
  1. Aby określić kierunek ekspozycji wprowadź odpowiednie kierunki oddzielone przecinkiem, spacją albo średnikiem. Wielkość liter jest bez znaczenia.
Patrz obrazek poniżej. ![http://wiki.qazp.googlecode.com/hg/imgs/ed_ekspo.png](http://wiki.qazp.googlecode.com/hg/imgs/ed_ekspo.png)
  1. Przed przejściem do innej kategorii dane należy zapisać klikając na przycisk **Save**.
  1. Edytor stanowisk można opuścić klikając na przycisk **Close** nie zapominając o zapisaniu zmian.

# Edycja faktów kulturowych #
Edycja faktów kulturowych polega na określaniu funkcji oraz chronologii z konotacją kulturową dla zebranych przedmiotów.
![http://wiki.qazp.googlecode.com/hg/imgs/ed_fakty2.png](http://wiki.qazp.googlecode.com/hg/imgs/ed_fakty2.png)
  1. Wyszukaj i wybierz stanowisko, dla którego mają być wprowadzone informacje o faktach kulturowych.
  1. Przejdź do edycji właściwości stanowiska przyciskiem **Edytuj**.
  1. Kliknij na przycisk **Fakty** aby wyświetlić edytor faktów.
  1. Jeżeli chcesz dodać nowy fakt kliknij na ostani (pusty) wiersz tabeli.
  1. Jeżeli chcesz zmienić albo usunąć fakt wybierz odpowiedni z listy.
  1. Dla wybranej właściwości (chronologia, kultura, funkcja, masowy, wydzielony) wprowadź odpowiednie wartości wpisując je w pola tekstowe albo wybierając odpowiednie z listy.
  1. Jeżeli przedmiot pochodzi z przełomu dwóch kultur albo dwóch okresów chronologicznych wybierz odpowiednie wartości z list rozwijanych, które znajdują się pod określoną kolumną tabeli a następnie wskaż odpowiednią relację: **/** albo **-** wybierając ją z listy rozwijanej.
  1. Jeżeli określenie chronologii, kultury albo funkcji jest niepewne wprowadź w polu tekstowym pod odpowiednią kolumną tabeli wartość. 1 - oznacza 100 procent pewności, 0.01 oznacza najmniejszą możliwą pewność.
  1. Aby dodać fakt, albo zapisać zmiany **w bazie danych** należy kliknąć przycisk **Dodaj**.
  1. Aby usunąć _zapisany_ fakt naciśnij przycisk **Usuń**
  1. Przed opuszczeniem edytora należy zatwierdzić wprowadzone zmiany klikając na przycisk **Save**. UWAGA! Niezatwierdzone zmiany zostaną utracone!

**Procedura wprowadzania faktów kulturowych została także przedstawiona na krótkim [filmie](http://www.youtube.com/watch?v=jLc4Ua4JgPY).**

# Generowanie kart KEZA #
QAZP2 umożliwia generowanie kart KEZA zgodnych z rozporządzeniem Ministra Kultury i Dziedzictwa Narodowego. Wygenerowane karty zapisywane są w pliku PDF w wybranej lokalizacji.
  1. Wyszukaj stanowiska, dla których mają być generowane karty
  1. Naciśnij przycisk **Drukuj**
  1. Podaj nazwę pliku, w którym mają być zapisane wygenerowane karty.
  1. Naciśnij przycisk **Save** i czekaj na komunikat o wygenerowaniu kart.

# Filtrowanie stanowisk #
Listę wyszukanych stanowisk można odfiltrować według wybranych kryteriów.
  1. Wyszukaj stanowiska wybierając odpowiednią opcję z menu **Stanowiska**
  1. Naciśnij przycisk **Filtruj**
  1. Wprowadź kryteria wybierając kolejno tabelę, która zawiera kolumnę według której wartości będą filtrowane dane, następnie nazwę kolumny, a na końcu wartość wskazując ją na rozwijanej liście albo wprowadzając w polu tekstowym.
  1. Zatwierdź przyciskiem **OK**

Odfiltrowane stanowiska można wyświetlić na nowej warstwie, na przykład w celu określenia ich rozkładu w przestrzeni używając przycisku **Wyświetl**

**Procedura filtrowania stanowisk została także przedstawiona na krótkim [filmie](http://www.youtube.com/watch?v=Q_kVYRLnP-k).**

# Tworzenie zestawień #
QAZP2 umożliwia tworzenie zestawień w celu zliczania stanowisk i grupowania ich według wybranych kryteriów.
  1. Z menu **Zestawienia** wybierz **Nowe zestawienie**
  1. Zostaje wyświetlony edytor zestawień. Składa się z dwóch części: górnej - tabeli, w której tworzy się zestawienie oraz dolnej, w której wyświetlane jest polecenie SQL utworzone na podstawie wyboru użytkownika.
  1. W pierwszej kolumnie **Funkcja** wybierz funkcję agregującą (na obecną chwilę dostępna jest tylko funkcja zliczająca LICZ().
  1. W drugiej kolumnie wybierz tabele i pola według których będą grupowane wyniki. Można dodać dowolną liczbę pól.
  1. (Opcjonalne) W kolejnych kolumnach dodaj parametry, które oznaczają stanowiska, które mają być uwzględnione w zestawieniu. Parametry znajdujące się w tym samym wierszu będą połączone operatorem OR (LUB). Parametry z wierszy zostaną powiązane operatorem AND (ORAZ).
**Przykład** Aby wybrać stanowiska które mają małą albo średnią wartości i są na obszarze 01-21, w pierwszym wierszu w kolumnie ORAZ należy wybrać pole _Wnioski.Wartość_. To samo pole należy wybrać w następnej kolumnie w tym samym wierszu. W wierszu poniżej, w kolumnie ORAZ należy wybrać pole _Stanowisko.Obszar AZP_.
  1. Naciśnij przycisk **Dalej**
  1. Jeżeli zostały okrślone parametry wyszukiwania (w kolumnach ORAZ i LUB) należy podać konkretne wartości, według których będą wyszukiwane stanowiska.
  1. Po wykonaniu polecenia SQL z podanymi parametrami zostają wyświetlone wyniki.
  1. Do edytora poleceń można powrócić klikając przycisk **Wstecz**
  1. Aby wydrukować zestawienie do pliku PDF naciśnij przycisk **Drukuj**
**Procedura tworzenia zestawień została także przedstawiona na krótkim [filmie](http://youtu.be/2SHFu3FOjC0).**