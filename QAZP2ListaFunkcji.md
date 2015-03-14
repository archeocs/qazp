# lista funkcji programu QAZP2

# O programie #

Program QAZP2 służy do zarządzania informacjami (dodawania, usuwania, modyfikowania oraz przetwarzania) pochodzącymi z badań archeologicznych. Informacje są zapisywane ze współrzędnymi w przestrzennej bazie danych (Spatialite / PostGIS) i wyświetlane w programie QuantumGIS.

# Lista funkcji #

Funkcje programu QAZP2 zostały opisane z podziałem na problematykę, której dotyczą.

**Program znajduje się w fazie rozwoju i jego funkcjonalność ulega dynamicznym zmianom**

## Miejsca ##

Miejscami nazywane są punkty na mapie, które zostały naniesione w trakcie badań terenowych z uwagi na ich szczególne znaczenie. Każde miejsce ma przypisane współrzędne oraz podstawowe informacje takie jak nazwa (ułatwiająca wyszukiwanie), datę dodania, autora (osobę, która zarejestrowała / naniosła punkt na mapę) oraz uwagi, w których można zawrzeć dodatkowe informacje.

### Funkcje ###

  1. Dodawanie miejsc do przestrzennej bazy danych:
    * bezpośrednio z odbiornika GPS na podstawie plików GPX,
    * przez nanoszenie punktów w programie QuantumGIS.
  1. Edycja informacji dotyczących miejsca:
    * Nazwy,
    * Autora,
    * Daty rejestracji,
    * Rodzaju badań,
    * Inny uwag.
  1. Wyszukiwanie miejsc według wybranych kryteriów i wyświetlanie ich na mapie w programie QuantumGIS.

## Trasy ##
Trasy służą do oznaczania drogi przebytej w trakcie badań archeologicznych, zarejestrowanej przy pomocy odbiornika GPS. Każda trasa składa się z segmentów (punktów pomiarowych GPS połączonych linią prostą, które są zapisywane z częstotliwością ustawioną w urządzeniu). Dla każdej trasy można podać rodzaj badań (np. powierzchniowe, lotnicze, itp.), moment rozpoczęcia, moment zakończenia, datę prowadzenia badań, autora, częstotliwość zapisu punktów oraz dodatkowe uwagi.

### Funkcje ###

  1. Dodawanie tras do przestrzennej bazy danych na podstawie odczytu z odbiornika GPS.
  1. Edycja informacji dotyczących tras:
    * Nazwy,
    * Autora,
    * Daty rejestracji,
    * Rodzaju badań,
    * Inny uwag.
  1. Wyszukiwanie tras według wybranych kryteriów i wyświetlanie ich na mapie w programie QuantumGIS.

## Stanowiska ##

Stanowiska na mapie są przedstawiane jako wielokąty (_poligony_) i służą do oznaczania wszystkich pozostałości osadnictwa człowieka. Program QAZP2 umożliwia dodawanie **pełnej informacji** o stanowiskach archeologicznych, która jest wymagana w sprawozdaniach z przeprowadzonych badań i drukowana na Karcie Ewidencji Zabytku/Stanowiska Archeologicznego (KEZA / KESA).

### Funcje ###

  1. Dodawanie stanowisk przez nanoszenie poligonów w programie QuantumGIS.
  1. Zarządzanie informacjami (dodawanie, usuwanie, modyfikowanie) o stanowisku archeologicznym.
  1. Tworzenie i drukowanie seryjne Kart Ewidencji Zabytku Archeologicznego **zgodnych ze wzorem Ministra Kultury i Dziedzictwa Narodowego** na podstawie informacji z przestrzennej bazy danych.
  1. Wyszukiwanie stanowisk.
  1. Filtrowanie stanowisk według wybranych kryteriów.
  1. Tworzenie zestawień