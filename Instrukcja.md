# Przygotowanie do pracy #

Jeśli wtyczka jest już zainstalowana w QuantumGIS, z menu _Plugins->QAZP_ należy wybrać QAZP. Przed tym należy zdefiniować conajmniej jedno połączenie z przestrzenną bazą danych Postgis lub Spatialite. W tym celu należy z menu _Layer_
wybrać _Add Postgis Layer_ lub odpowiednio _Add Spatialite Layer_.
Domyślnie QAZP w pierwszej kolejności otwiera wybraną bazę Spatialite, można jednak to zmienić w ustawieniach programu.


# Praca z QAZP #

W tej sekcji zostały opisane zasady korzystania z przestrzennej bazy danych (PBD) przy pomocy programu QAZP i QuantumGIS

## Dodawanie stanowiska ##

Terminem **Stanowisko** określa się jednorazową identyfikację stanowiska w lokalizacji, którą określa arkusz AZP i numer. Z pojedynczą lokalizacją może być związanych więcej niż jedno **Stanowisko** - na przykład pierwsza kwerenda archiwalna, zdjęcie lotnicze, weryfikacja, itd.

**Procedura dodawania stanowiska**
  1. W programie QuantumGIS zaznacz położenie i kształ badanego stanowiska
  1. W wyświetlonym oknie dialogowym wprowadź następujące informacje
    * Rodzaj - litera zgodnie ze standardem AZP
    * arkusz - numer arkusza AZP
    * nr\_arkusz - numer stanowiska w obrębie arkusza AZP
    * miejscowosc - nazwa miejscowości
    * nr\_miejscowosc - numer stanowiska w obrębie miejscowości
    * autor - autor badań, które reprezentuje utworzone stanowisko
    * data - data badań w formacie RRRR-MM-DD
> Wartości w polach **sid** oraz **lokalizacja** powinny pozostać puste.
  1. Naciśnij przycisk OK
  1. Zapisz zmiany

Jest to jedyna metoda dodawania stanowisk do przestrzennej bazy danych. Program QAZP umożliwia wyłącznie modyfikację wprowadzonych stanowisk. Dane należy wprowadzić w taki sposób, by umożliwiały łatwą identyfikację stanowiska w QAZP. Dotyczy to przede wszystkim numeru arkusza i numeru stanowiska w jego obrębie.

## Przeglądanie stanowisk ##

Wprowadzone stanowiska można przeglądać posługując się numerem arkusza i numerem stanowiska w jego obrębie.

**Procedura przeglądania stanowisk**
  1. Z listy _Arkusz_ wybierz numer arkusza
  1. Z listy _Nr na arkuszu_ wybierz numer AZP stanowiska (opcjonalne)
  1. Kliknij przycisk _Filtruj_

W tabeli wyświetlane są podstawowe informacje o stanowiskach, takie jak nazwa miejscowości, numer stanowiska w miejscowości, data badań, nazwa autora badań. Po zaznaczeniu stanowiska i kliknięciu przycisku _Szczegóły_ wyświetlane są dotyczące go dane z karty KESA.

## Lokalizacja stanowiska ##

Po zaznaczeniu kształtu stanowiska i jego położenia na mapie w programie QuantumGIS należy przypisać je do lokalizacji, jeśli taka istnieje, lub utworzyć nową, jeśli w bazie nie ma informacji o poprzednich badaniach.

### Tworzenie słowników nazw ###

Aby dane w PBD pozostawały spójne wszystkie nazwy własne, takie jak nazwy miejscowości, województ, kultur, funkcji osadniczych, itp. są zapisywane w postaci słowników. W QAZP stosuje się dwa rodzaje słowników. W menu _Lokalizacje_ znajdują się te, które służą do określania lokalizacji stanowiska, czyli: nazwy miejscowości, gmin, powiatów oraz województw. W menu _Klasyfikacja_ znajdują się słowniki używane przy wprowadzaniu faktów kulturowych: nazwy epok, kultur i funkcji osadniczych. Każdy z wymienionych słowników można modyfikować, to znaczy dodawać nowe nazwy oraz zmieniać i usuwać już istniejące.

**Procedura dodawania nazwy do słownika** (na przykładzie Miejscowości)
  1. Z menu _Lokalizacje_ wybierz _Miejscowości_
  1. Kliknij przycisk _Dodaj_
  1. Wprowadź nazwę miejscowości (wielkość liter nie ma znaczenia)
  1. Kliknij przycisk _OK_
  1. Aby dodać kolejną nazwę przejdź do punktu 2.
  1. Aby zamknąć słownik i zatwierdzić wszystkie zmiany kliknij przycisk _Save_
  1. Aby zamknąć słownik i wycofać zmiany kliknij przycisk _Cancel_

### Określanie lokalizacji ###

Określenie lokalizacji stanowiska ma kluczowe znaczenie, gdyż pozwala zachować spójność bazy i jednolitość nazewnictwa. Stanowiska bez określonej lokalizacji nie są uwzględniane w większości zdefiniowanych zestawień.

**Procedura określania lokalizacji**
  1. Wyszukaj nowe stanowisko (patrz rozdział [Instrukcja#Przeglądanie\_stanowisk] )
  1. Zaznacz stanowisko na liście i kliknij przycisk _Lokalizacja_
  1. Jeśli arkusz i numer na arkuszu są nieprawidłowe, wprowadź poprawne wartości.
  1. Jeśli informacja o innych badaniach na wskazanym stanowisku znajdują się już w bazie kliknij przycisk _Znajdź_. Jeśli w bazie znajduje się lokalizacja dla podanego arkusza i numeru odpowiednie pola zostaną wypełnione prawidłowymi wartościami i można przejść do punktu 6. W przeciwnym wypadku przejdź do punktu 5.
  1. Wprowadź poprawne wartości. Wszystkie pola muszą być wypełnione. Jeśli brakuje nazwy na liście, należy przerwać wprowadzanie lokalizacji i uzupełnić odpowiedni słownik (Patrz rozdział [Instrukcja#Tworzenie\_słowników\_nazw Tworzenie słowników nazw])
  1. Zapisz lokalizację

## Informacje o stanowisku ##

Przy pomocy QAzp użytkownicy mogą przeglądać dane z karty Azp. W tym celu należy wyszukać stanowisko, a następnie kliknąć przycisk _Szczegóły_. Większość cech jest wyświetlana w postaci list składających się z dwóch wartości TAK i NIE. Jeśli stanowisko ma określoną cechę, to wyświetlana jest przy niej wartość TAK. Jeśli nie posiada cechy, lub nie zostało to określone, wybrane jest NIE. Użytkownik zmienia wartości wybierając odpowiednią z listy.

Wartości pogrupowane są tematycznie w karty.

### Fakty kulturowe ###

Na karcie _Fakty kulturowe_ wyświetlane są fakty kulturowe pochodzące z przeglądanego stanowiska. Wyświetlane są w postaci tabeli. Zawiera ona wartości pochodzące ze słowników, wartości tekstowe oraz wartości numeryczne.

**Procedura dodawania faktu**
  1. Przejdź do wiersza, który w kolumnie _Epoka_ ma wartość 

&lt;Nowy&gt;

