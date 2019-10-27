/*
 * (c) Milosz Piglas 2012 Wszystkie prawa zastrzezone

 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are
 *  met:
 *
 *      * Redistributions of source code must retain the above copyright
 *  notice, this list of conditions and the following disclaimer.
 *      * Redistributions in binary form must reproduce the above
 *  copyright notice, this list of conditions and the following disclaimer
 *  in the documentation and/or other materials provided with the
 *  distribution.
 *      * Neither the name of Milosz Piglas nor the names of its
 *  contributors may be used to endorse or promote products derived from
 *  this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 *  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 *  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 *  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 *  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 *  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

package main

import (
	"database/sql"
	"fmt"
	"log"
	"strings"

	"github.com/mattn/go-sqlite3"
)

var (
	wspDb                                                                   *sql.DB
	azpDb                                                                   *sql.DB
	mwyk, gwyk, pwyk, wwyk                                                  *wykaz
	stps, geops, fgps, ekps, obps, wnps, teps, zaps, akps, gbps, kaps, fkps *sql.Stmt
	tabids                                                                  = make(map[string]int)
)

// Tworzy nastepny identyfikator dla nowego rekordu w wykazach miejscowosci, gmin, powiatow
// i wojewodztw. Jezeli w tych tabelach w bazie sa juz jakies wpisy, to sa one brane pod uwage
func nastId(tab string) int {
	var (
		ost int
		ok  bool
	)
	if ost, ok = tabids[tab]; !ok {
		r := azpDb.QueryRow("select coalesce(max(id),0) from " + tab)
		r.Scan(&ost)
	}
	tabids[tab] = ost + 1
	return ost + 1
}

func initSpatialiteDriver() {
	sql.Register("spatialite", &sqlite3.SQLiteDriver{
		ConnectHook: func(conn *sqlite3.SQLiteConn) error {
			err := conn.LoadExtension("mod_spatialite", "sqlite3_modspatialite_init")
			if err == nil {
				return nil
			}
			return err
		},
	})
}

// Inicjalizuje polaczenie z bazami danych i wczytuje rozszerzenie spatialite (sterownik
// musi na to pozwalac
func initDb(wspSciez, azpSciez string) (de error) {
	// var r sql.Result
	initSpatialiteDriver()
	wspDb, de = sql.Open("spatialite", wspSciez)
	if de != nil {
		return
	}
	azpDb, de = sql.Open("spatialite", azpSciez)
	if de != nil {
		return
	}
	log.Println("DB INIT OK")
	return
}

// Inicjalizuje wykaz przez pobranie z niego rekordow i zapisanie
// ich w strukturze
func initWykaz(nazwa string) (wyk *wykaz, we error) {
	// wykaz = make(map[string]int)
	wyk = new(wykaz)
	wyk.mapa = make(map[string]int)
	wyk.ostatni = 0
	wyk.nazwa = nazwa
	var (
		r  *sql.Rows
		nw string
		ni int
	)
	r, we = azpDb.Query("select nazwa, id from " + nazwa)
	if we != nil {
		return
	}
	for r.Next() {
		r.Scan(&nw, &ni)
		if ni > wyk.ostatni {
			wyk.ostatni = ni
		}
		wyk.mapa[nw] = ni
	}
	r.Close()
	return
}

func initStmt() (se error) {
	stps, se = azpDb.Prepare("insert into stanowiska(id, obszar, nr_obszar, miejscowosc, nr_miejscowosc, gmina, powiat, wojewodztwo, data, autor, rodzaj_badan, uwagi, wspolrzedne) values (?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, st_polygonfromtext(?,2180))")
	geops, se = wspDb.Prepare("select astext(wspolrzedne) from stanowiska where obszar=? and nr_obszar=?")
	fgps, se = azpDb.Prepare("INSERT INTO fizgeo_dane(id, stanowisko, nadmorska, w_morzu, plaza, mierzeja, skarpa, wal_wydmowy, duze_doliny, w_wodzie, ter_denna, ter_nadzalewowa, ter_wyzsze, brzeg_wysoczyzny, male_doliny, dno_doliny, stok_doliny, krawedz_doliny, poza_dolinami, rownina, obsz_falisty, obsz_pagorkowaty, obsz_gorzysty, uwagi) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,  ?, ?)")
	ekps, se = azpDb.Prepare("INSERT INTO ekspozycja_dane VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
	obps, se = azpDb.Prepare("insert into obszar_dane(id, stanowisko, obserwacja, pole, nasyc_rozklad, nasyc_typ, powierzchnia, gestosc_znal, uwagi) values(?, ?, ?, ?, ?,  ?, ?, ?, ?)")
	teps, se = azpDb.Prepare("insert into teren_dane(id, stanowisko, zabudowany, sred_zabud, las, sad, park, pole_orne, laka, prywatny, spoleczny, przemyslowy, uwagi) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
	wnps, se = azpDb.Prepare("insert into wnioski(id, stanowisko, wartosc, inwentaryzacja, wykopaliska, interwencja, uwagi) values (?,?,?,?,?,?,?)")
	zaps, se = azpDb.Prepare("insert into zagrozenia(id, stanowisko, wystepowanie, czas, przyczyna_ludzie, przyczyna_natura, uzytkownik_spoleczny, uzytkownik_prywatny, uwagi) values(?,?,?,?,?,?,?,?,?)")
	akps, se = azpDb.Prepare("insert into aktualnosci(id, stanowisko, magazyn, nr_inwentarza) values (?, ?, ?,?)")
	gbps, se = azpDb.Prepare("insert into gleba_dane(id, stanowisko, luzna, zwiezla, torf_bag, kamienistosc, uwagi) values (?,?,?,?,?,?,?)")
	kaps, se = azpDb.Prepare("insert into karty(id,stanowisko,nazwa_lok,arkusz_mapy, dalsze_losy, dzieje_badan, literatura, autorzy, chronologia, konsultant) values (?,?,?,?,?,?,?,?,?,?)")
	fkps, se = azpDb.Prepare("insert into fakty(id,stanowisko,okresa,okresb,okr_relacja,okr_pewnosc,jeda,jedb,jed_relacja,jed_pewnosc,funkcja,fun_pewnosc,masowy,wydzielony) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
	return
}

func toString(v interface{}) string {
	return fmt.Sprintf("%#v", v)
}

// Dodaje do bazy danych informacje ze struktury implementujacej interfejs Tabela
// wykorzystujac do tego przygotowane polecenie SQL
func dodaj(ps *sql.Stmt, t Tabela, spr bool) (ei error) {
	tp := t.Params()
	zapisz := false
	if spr {
		for i := 2; i < len(tp); i++ {
			if tp[i] != nil {
				zapisz = true
				break
			}
		}
		if !zapisz {
			return
		}
	}
	_, ei = ps.Exec(tp...)
	if ei != nil {
		log.Printf("Error %s\n\n", toString(t))
		panic(ei.Error())
		//fmt.Println(ei.Error())
	}
	return
}

// Pobiera z wykazu identyfikator dla podanego klucza. Jezeli takiego klucza jeszcze
// nie ma, to dodaje go do wykazu i generuje dla niego nowy, unikatowy identyfikator
func (w *wykaz) ident(klucz string) (ni int) {
	var ok bool
	uk := strings.ToUpper(klucz)
	if len(uk) < 2 {
		ni = -1
		return
	}
	ni, ok = w.mapa[uk]
	if ok {
		return
	}
	_, e := azpDb.Exec("insert into "+w.nazwa+" values(?, ?, ?)", w.ostatni+1, uk[:2], uk)
	if e != nil {
		panic("Nie moge wstawic do wykazu ")
	}
	w.ostatni += 1
	ni = w.ostatni
	w.mapa[uk] = ni
	return
}
