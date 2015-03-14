#struktura danych w programie Azp Max

# Informacje #

W każdej kartotece stanowisk znajdują się dwie tabele DBF zapisane kodowaniem Windows-1250. Tabela AZP1XXX.DBF zawiera informacje o stanowisku, AZP2XXX.DBF informacje o zebranych faktach kulturowych. XXX oznacza nazwę kartoteki wybraną przez użytkownika.

## AZP1XXX.DBF ##

| Nazwa atrybutu | Opis | Uwagi |
|:---------------|:-----|:------|
| ` MIE ` | Nazwa miejscowości | Podawana każdorazowo przez użytkownika |
| ` GMI ` | Nazwa gminy | Podawana każdorazowo przez użytkownika |
| ` WOJ ` | Nazwa województwa | Wybierana z listy i zapisywana w postaci dwuznakowego kodu |
| ` NWJ ` | nazwa województwa według nowego podziału administracyjnego | jak wyżej |
| ` PWT ` | nazwa powiatu  | Wprowadzana przez użytkownika |
| ` NRO ` | numer obszaru azp | Podawany w postaci ` XXX-XX ` gdzie ` X ` oznacza cyfrę arabską |
| ` NSM ` | numer stanowiska w miejscowości  | Brak |
| ` NSO ` | numer stanowiska na obszarze | Brak |
| ` W25 ` | współrzędne w skali 1:25000 | Brak |
| ` LOK ` | nazwa lokalna | Brak |
| ` ZRO ` | rodzaj badań, których dotyczy karta | Pole zawiera ciąg, który może się skaładać z następujących znaków ` Z, R, A, T, W, P, L ` |
| ` NRI ` | numer inwentarza zabytków | Brak |
| ` REG ` | region geograficzny | Wprowadzany przez użytkownika |
| ` FIZ ` | położenie w obrębie jednostek fizjogeograficznych | Opisane ciągiem znaków, które mają następujące znaczenie: <br> 1 - strefa nadmorska (nadzalewowa) <br> A - w morzu <br> B - plaża <br> C - mierzeja <br> D - skarpa <br> E - wał wydmowy <br> 2 - duże doliny <br> F - w wodzie <br> G - terasy denne <br> H - terasy nadzalewowe <br> I - terasy wyższe <br> J - brzeg wysoczyzny <br> 3 - małe doliny <br> K - dno doliny <br> L - stok doliny <br> M - krawędź doliny <br> 4 - strefa poza dolinami <br> N - równina <br> O - obszar falisty <br> P - obszar pagórkowaty <br> Q - obszar górzysty <br>
<tr><td> <code> FOR </code> </td><td> forma szczególna </td><td> Wartość opisowa </td></tr>
<tr><td> <code> WEK </code> </td><td> wysokość ekspozycji </td><td> Atrybut może mieć następujące wartości: <br> 2 - ekspozycja bardzo mała ( 0-2 m) <br> 4 - eksp. mała (2-4 m) <br> 8 - eksp. umiarkowana (4-8 m) <br> 15 - eksp duża (8-15 m) <br> 20 - eksp. bardzo duża ( > 15 m) </td></tr>
<tr><td> <code> SEK </code> </td><td> stopień ekspozycji </td><td> Ciąg znaków o następującym znaczeniu: <br> 1 - 0-1% <br> 2 - 1-3% <br> 3 - 4-7% <br> 4 - 8-15% <br> 5 - > 15% </td></tr>
<tr><td> <code> KEK </code> </td><td> kierunki ekspozycji </td><td> Oznaczane następującymi literami: <br> A - N <br> B - NE <br> C - E <br> D - SE <br> E - S <br> F - SW <br> G - W <br> H - NW </td></tr>
<tr><td> <code> GLE </code> </td><td> Gleba </td><td> Ciąg znaków o następującym znaczeniu <br> 1 - piaszczysta <br> 2 - gliniasta <br> 3 - torfowo-bagienna </td></tr>
<tr><td> <code> KAM </code> </td><td> kamienistość </td><td> Dopuszczalne wartości: <br> M - mała <br> S - średnia <br> D - duża </td></tr>
<tr><td> <code> SPE </code> </td><td> określenie specjalistyczne </td><td> Opis </td></tr>
<tr><td> <code> TER </code> </td><td> dostępność terenu </td><td> Ciąg znaków, które mają następujące znaczenie <br> N - niezabudowany <br> S - średnio zabudowany <br> Z - zabudowany <br> 1 - las <br> 2 - sad <br> 3 - park <br> 4 - pole orne <br> 5 - łąka <br> 6 - teren rolniczy pryw <br> 7 - teren rolniczy społ. <br> 8 - teren przemysłowy </td></tr>
<tr><td> <code> TEB </code> </td><td> dostępność terenu - określenie bliższe </td><td> Opis </td></tr>
<tr><td> <code> OBS </code> </td><td> charakterystyka obszaru (obserwacja) </td><td> Dopuszczalne wartości: <br> 0 - utrudniona <br> 1 - bez przeszkód </td></tr>
<tr><td> <code> POL </code> </td><td> charakterystyka obszaru (pole) </td><td> Dopuszczalne wartości: <br> 0 - otwarte <br> 1 - zamknięte </td></tr>
<tr><td> <code> NAS </code> </td><td> charakterystyka obszaru (nasycenie znaleziskami) </td><td> Dopuszczalne wartości: <br> 0 - równomierne <br> 1 - nierównomierne </td></tr>
<tr><td> <code> CEN </code> </td><td> charakterystyka obszaru </td><td> Dopuszczalne wartości: <br> 0 - st. jednocentryczne <br> 1 - st. wielocentryczne <br> 2 - st. dekocentryczne </td></tr>
<tr><td> <code> POW </code> </td><td> powierzchnia stanowiska (ha) </td><td> Dopuszczalne wartosci: <br> 0 - 0 <br> 0.01 - poniżej 0.01 <br> 0.5 - poniżej 0.5 <br> 1 - poniżej 1 <br> 5 - poniżej 5 <br> 15 - poniżej 15 <br> 20 - powyżej 15 </td></tr>
<tr><td> <code> GES </code> </td><td> gęstość występowania znalezisk </td><td> Dopuszczalne wartości <br> M - mała <br> S - średnia <br> D - duża </td></tr>
<tr><td> <code> ZAG </code> </td><td> zagrożenie 1 </td><td> Dopuszczalne wartości: <br> 0 - nie istnieje <br> 1 - istnieje </td></tr>
<tr><td> <code> ZAC </code> </td><td> zagrożenie 2 </td><td> Dopuszczalne wartości:  <br> 0 - doraźne <br> 1 - stałe </td></tr>
<tr><td> <code> ZAK </code> </td><td> zagrożenie 3 </td><td> Dopuszczalne wartości:  <br> L - przez ludzi <br> N - przez naturę </td></tr>
<tr><td> <code> ZAU </code> </td><td> zagrożenie 4 </td><td> Dopuszczalne wartości:  <br> P - przez użytkownika prywatnego <br> N - przez użytkownika społecznego </td></tr>
<tr><td> <code> ZUW </code> </td><td> zagrożenie dane dodatkowe </td><td> Opis </td></tr>
<tr><td> <code> WAR </code> </td><td> ocena wartości poznawczej stanowiska </td><td> Dopuszczalne wartości: <br> M - mała <br> S - średnia <br> D - duża </td></tr>
<tr><td> <code> WNI </code> </td><td> wnioski konserwatorskie </td><td> Dopuszczalne wartości:  <br> 1 - niezbędna szczegółowa inwentaryzacja <br> 2 - niezbędne wykopaliska <br> 3 - niezbędna interwencja administracyjna </td></tr>
<tr><td> <code> WND </code> </td><td> wnioski: dane dodtkowe </td><td> Opis </td></tr>
<tr><td> <code> DAT </code> </td><td> data badań </td><td> W postaci MMRR </td></tr>
<tr><td> <code> AUT </code> </td><td> autorzy badań </td><td> Brak </td></tr>
<tr><td> <code> OCH </code> </td><td> określił chronologię </td><td> Brak </td></tr>
<tr><td> <code> SPR </code> </td><td> sprawdził </td><td> Brak </td></tr>
<tr><td> <code> ZBI </code> </td><td> miejsce przechowywania materiałów </td><td> Brak </td></tr>
<tr><td> <code> DAL </code> </td><td> informacje o dalszych losach stanowiska </td><td> Brak </td></tr>
<tr><td> <code> BAD </code> </td><td> wcześniejsze badania </td><td> Brak </td></tr>
<tr><td> <code> LIT </code> </td><td> literatura </td><td> Brak </td></tr>
<tr><td> <code> MAP </code> </td><td> godło mapy </td><td> Brak </td></tr>
<tr><td> <code> W1X </code> </td><td> współrzędne X </td><td> Brak </td></tr>
<tr><td> <code> W1Y </code> </td><td> współrzędne Y </td><td> Brak </td></tr>
<tr><td> <code> MHM </code> </td><td> źródła historyczne </td><td> Brak </td></tr>
<tr><td> <code> UWA </code> </td><td> Uwagi </td><td> Brak </td></tr>
<tr><td> <code> ILF </code> </td><td> Liczba faktów kulturowych </td><td> Brak </td></tr>
<tr><td> <code> SEL </code> </td><td> Pole systemowe </td><td> Brak </td></tr>
<tr><td> <code> SEL1 </code> </td><td> Pole systemowe </td><td> Brak </td></tr>
<tr><td> <code> WSP </code> </td><td> współrzędne na mapie 1:10000 </td></tr></tbody></table>

<h2>AZP2XXX.DBF</h2>

<table><thead><th> Nazwa atrybutu </th><th> Opis </th><th> Uwagi </th></thead><tbody>
<tr><td> <code> NRF </code> </td><td> Numer porządkowy w ramach stanowiska </td><td> Przydzielany automatycznie </td></tr>
<tr><td> <code> FUN </code> </td><td> Funkcja obiektu </td><td> Nazwa wybierana z listy </td></tr>
<tr><td> <code> KUL </code> </td><td> Kultura </td><td> Nazwa wybierana z listy </td></tr>
<tr><td> <code> CHN </code> </td><td> Chronologia </td><td> Nazwa wybierana z listy </td></tr>
<tr><td> <code> MAM </code> </td><td> Materiały masowe </td><td> Wpisywane przez użytkownika </td></tr>
<tr><td> <code> MAW </code> </td><td> Materiały wyodrębnione </td><td> Wpisywane przez użytkownika </td></tr>
<tr><td> <code> NRR </code> </td><td> Identyfikator stanowiska </td><td> Numer obszaru AZP i numer w ramach obszaru rozdzielone spacją </td></tr>