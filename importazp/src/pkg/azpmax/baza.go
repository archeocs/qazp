package main

import (
    _ "github.com/mattn/go-sqlite3"
    "database/sql"
    "fmt"
    "strings"
)

var (
    wspDb *sql.DB
    azpDb *sql.DB
    mwyk, gwyk, pwyk, wwyk *wykaz
    stps, geops, fgps, ekps, obps, wnps, teps, zaps, akps, gbps, kaps, fkps *sql.Stmt
    tabids = make(map[string]int)
)

func nastId(tab string) int {
    var (
        ost int
        ok bool
    )
    if ost, ok = tabids[tab]; !ok {
        r := azpDb.QueryRow("select coalesce(max(id),0) from "+tab)
        r.Scan(&ost)
    }
    tabids[tab] = ost+1
    return ost+1
}

func initDb(wspSciez, azpSciez string) (de error) {
    // var r sql.Result
    wspDb, de = sql.Open("sqlite3", "/home/milosz/archeocs/import_azpmax/"+wspSciez)
    if de != nil {
        return
    }
    azpDb, de = sql.Open("sqlite3", "/home/milosz/archeocs/import_azpmax/"+azpSciez)
    if de != nil {
        return 
    }
    _, de = wspDb.Exec("select load_extension('libspatialite.so.3')")
    if de != nil {
        return
    }
    _, de = azpDb.Exec("select load_extension('libspatialite.so.3')")
    if de != nil {
        return
    }
    fmt.Println("DB INIT OK")
    return
} 

func initWykaz(nazwa string) (wyk *wykaz, we error) {
    // wykaz = make(map[string]int)
    wyk = new(wykaz)
    wyk.mapa = make(map[string]int)
    wyk.ostatni = 0
    wyk.nazwa = nazwa
    var (
        r *sql.Rows
        nw string
        ni int
    )
    r, we = azpDb.Query("select nazwa, id from "+nazwa)
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

func dodaj(ps *sql.Stmt, t Tabela, spr bool) (ei error) {
    tp := t.Params()
    zapisz := false
    if spr {
        for i:=2; i < len(tp); i++ {
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
		panic(ei.Error())
		//fmt.Println(ei.Error())
	}
	return
}

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
    _, e := azpDb.Exec("insert into "+w.nazwa+" values(?, ?, ?)",w.ostatni+1, uk[:2], uk)
    if e != nil {
        panic("Nie moge wstawic do wykazu ")
    }
    w.ostatni += 1
    ni = w.ostatni
    w.mapa[uk] = ni
    return
}

