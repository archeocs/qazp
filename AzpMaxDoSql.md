#import danych z programu Azpmax do relacyjnej bazy danych

# Opis programu #

Program pobiera dane zapisane w programie Azpmax, łączy je z danymi przestrzennymi utworzonymi w programie QGIS i zapisuje do bazy SQLITE, której schemat umożliwia stosowanie z wtyczką QAZP2. W aktualnej wersji nie są wspierane alternatywne systemy takiej jak PostrgreSQL albo MySQL.

# Przygotowanie #

Przed rozpoczęciem importu należy wykonać kilka prostych czynności.
  1. Zainstalować kompilator języka [Go](http://golang.org).
  1. Zainstalować [sterownik](https://github.com/mattn/go-sqlite3) do bazy sqlite
  1. Utworzyć bazę ze współrzędnymi korzystając z narzędzia [spatialite-tools](https://www.gaia-gis.it/fossil/spatialite-tools). Współrzędne powinny być zapisane w tabeli o nazwie _STANOWISKA_, w kolumnie _WSPOLRZEDNE_. Każdy rekord powinny jednoznacznie identyfikować numer obszaru AZP w kolumnie _OBSZAR_ i numer stanowiska w ramach obszaru zapisany w kolumnie _NR\_OBSZAR_.
  1. Zapisać dane Azpmax w formacie CSV, gdzie wartości są rozdzielone znakiem _#_.
  1. Nazwy okresów chronologicznych, funkcji oraz jednostek kulturowych powinny być zastąpione odpowiednimi kodami z wykazów.
  1. Pobrać kod [źródłowy](http://qazp.googlecode.com/files/import_azpmax-src.zip) programu do importu.
  1. Pobrać [pustą](http://qazp.googlecode.com/files/azp2_lite-0.11.zip) bazę sqlite z przygotowanym schematem tabel.

# Uruchomienie programu #
Aby uruchomić program należy przejść do katalogu src/pkg/azpmax i z lini poleceń wykonać komendę sh start.sh