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
    "os"
    "bufio"
    "strings"
    "fmt"
    "strconv"
    "time"
    "math"
    "errors"
    "flag"
    )

const (
    dtfmt string = "02/01/06"
    dbdtfmt string = "2006-01-02"
)

var (
	maxZam = map[string]string {"A0":"U", "A1":"B", "A":"", "B0":"O", "B1":"Z", "B":"", "C0":"R", "C1":"N", "C":"", "D0":"J", "D1":"W", "D2":"D", "D":"", "E1":"I", "E0":"N", "E":"", "F1":"D", "F0":"S", "F":"", "GL":"L", "GN":"N", "G":"", "HP":"P", "HS":"S", "H":"", "JM":"M", "JS":"S", "JD":"D", "J":""}
	faktyPlik, stPlik, bazaPlik, wspPlik string
)

func NewCsv(sciezka string) (dane *csv, err error) {
    dane = new(csv)
    if dane.plik, err = os.Open(sciezka); err != nil {
        return
    }
    dane.rd = bufio.NewReader(dane.plik)
    return
}


func (dane *csv) Wiersz() (tabs []string, nastepny bool) {
    if linia, re := dane.rd.ReadString('\n'); re == nil {
        tabs = strings.Split(linia,"#")
        nastepny = true

    } else {
        dane.plik.Close()
        nastepny = false
    }
    return
}

func NewWiersz(tabs []string) (cw wiersz) {
    cw = wiersz{miej:trim(tabs[0]), gm:trim(tabs[1]), woj:trim(tabs[2]), obsz:trim(tabs[5]), nrobsz:trim(tabs[7]), nrmiej:trim(tabs[6]), nazlok:trim(tabs[9]), rodzbad:trim(tabs[10]), databad:trim(tabs[38]), autor:trim(tabs[39]), region:trim(tabs[12]), jedfiz:trim(tabs[13]), rodzeks:trim(tabs[14]), wyseks:trim(tabs[16]), kiereks:trim(tabs[18]), stopeks:trim(tabs[17]), forszczeg:trim(tabs[15]), doster:trim(tabs[22]), blizter:trim(tabs[23]), obser:trim(tabs[24]), poleobsz:trim(tabs[25]), nasycrozk:trim(tabs[26]), nasyctyp:trim(tabs[27]), obszpow:trim(tabs[28]), gest:trim(tabs[29]), zagwys:trim(tabs[30]), zagczas:trim(tabs[31]), zagprzy:trim(tabs[32]), zaguz:trim(tabs[33]), zaguw:trim(tabs[34]), wart:trim(tabs[35]), wnio:trim(tabs[36]), wniodod:trim(tabs[37]), chrono:trim(tabs[40]), konsul:trim(tabs[41]), magazyn:trim(tabs[42]), losy:trim(tabs[43]), hisbad:trim(tabs[44]), nrinw:trim(tabs[11]), liter:trim(tabs[45]), godlo:trim(tabs[46]), uwagi:trim(tabs[50]), gleba:trim(tabs[19]), kam:trim(tabs[20]), glespec:trim(tabs[21]), zrodla:trim(tabs[49]), nwoj:trim(tabs[3]), powiat:trim(tabs[4])}
    return
}

func trim(s string) string {
    return strings.TrimSpace(s)
}

func stof(s string) (float32, error) {
    if s == "" {
        return 0, nil
    }
    f, e := strconv.ParseFloat(s, 32)
    if e != nil {
        return -1, errors.New("Nieprawidlowy format liczby: "+s)
    }
    return float32(f), nil
}

func dekodRodz(r string) string {
    ur := strings.ToUpper(r)
    if strings.Contains(ur,"W") {
        return "W" 
    } else if strings.Contains(ur,"P") {
        return "P" 
    } else if strings.Contains(ur,"T") {
        return "T" 
    } else if strings.Contains(ur,"L") {
        return "L" 
    } else if strings.Contains(ur,"X") {
        return "X" 
    } else if strings.Contains(ur,"N") {
        return "N" 
    }
    return "?"
}

func stWsp(ob, nrob string) (geom string) {
    r := geops.QueryRow(ob, nrob)
    r.Scan(&geom)
    return
}

func tb(s string) []byte {
    return []byte(s)
}

func (w wiersz) newStanowisko() (stanowisko, error) {
    st := stanowisko{obszar:w.obsz, nrObszar:w.nrobsz, miejscowosc:mwyk.ident(w.miej), 
                        gmina:gwyk.ident(w.gm), powiat: pwyk.ident(w.powiat), rodzBad:dekodRodz(w.rodzbad),
                        autor:w.autor,  nrMiej:w.nrmiej, id:nastId("stanowiska"), uwagi:w.uwagi}
    if w.nwoj != "" {
        st.wojewodztwo = wwyk.ident(w.nwoj)
    } else {
        st.wojewodztwo = wwyk.ident(w.woj)
    }
    t, e := time.Parse(dtfmt, "01/"+w.databad)
    if e != nil {
        return st, e //panic(e.Error())
    } else {
        st.data = t.Format(dbdtfmt) 
    }
    st.geom = stWsp(st.obszar, st.nrObszar)
    return st, nil 
}

func (w wiersz) newEksdane(st int) (e eksdane) {
    e = eksdane{ stanowisko:st, id:nastId("ekspozycja_dane"), uwagi:w.forszczeg}
    dekodRodzEks(w.rodzeks, &e)
    //dekodRozmEks(w.wyseks, &e)
    dekodStopEks(w.stopeks, &e)
    dekodKierEks(w.kiereks, &e)
    f32, ferr := stof(w.wyseks)
    if ferr != nil {
        fmt.Println(ferr.Error())
    } 
    e.rozmiar = f32
    return
}

func dekodKierEks(d string, e *eksdane)  {
    var kiers = map[string]float64 {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}
    td := strings.Split(d, "")
    dkier := 0.0
    for i:=0; i < len(td); i++ {
        dkier += math.Pow(2,kiers[td[i]])
    }
    e.kierunek = int(dkier)
}

func dekodStopEks(d string, e *eksdane) {
    switch d {
        case "1": e.stopien = 0.5
        case "2": e.stopien = 2
        case "3": e.stopien = 5.5
        case "4": e.stopien = 11.5
        case "5": e.stopien = 16
        default: e.stopien = 0
    }
}

func dekodRodzEks(d string, e *eksdane) {
    td := strings.Split(d, "")
    for i := 0; i < len(td); i++ {
        switch td[i] {
            case "1": e.eksponowany = "T"
            case "A": e.kraw_stoki = "T"
            case "B": e.sfaldowania_cyple = "T"
            case "C": e.cyple_wybitne = "T"
            case "D": e.waly_garby = "T"
            case "E": e.wyniesienia_okrezne = "T"
            case "2": e.osloniety = "T"
            case "F":  e.podst_stoku = "T"
            case "G": e.doliny_niecki = "T"
            case "H": e.kotlinki_zagleb = "T"
            case "I": e.jaskinie = "T"
        }
    }
}

func (w wiersz) newFizgeo(st int) (f fizgeo) {
    f = fizgeo{uwagi:w.region, stanowisko:st, id:nastId("fizgeo_dane")}
    tj := strings.Split(w.jedfiz, "")
    for i := 0; i < len(tj); i++ {
        switch tj[i] {
            case "1": f.nadmorska = "T"
            case "A": f.w_morzu = "T"
            case "B": f.plaza = "T"
            case "C": f.mierzeja = "T"
            case "D": f.skarpa = "T"
            case "E": f.wal_wydmowy = "T"
            case "2": f.duze_doliny = "T"
            case "F":  f.w_wodzie = "T"
            case "G": f.ter_denna = "T"
            case "H": f.ter_nadzalewowa = "T"
            case "I": f.ter_wyzsze = "T"
            case "J": f.brzeg_wysoczyzny = "T"
            case "3": f.male_doliny = "T"
            case "K": f.dno_doliny = "T"
            case "L": f.stok_doliny = "T"
            case "M": f.krawedz_doliny = "T"
            case "4": f.poza_dolinami = "T"
            case "N": f.rownina = "T"
            case "O": f.obsz_falisty = "T"
            case "P": f.obsz_pagorkowaty = "T"
            case "Q": f.obsz_gorzysty = "T"
        }
    }
    return 
}

func (w wiersz) newObsdane(st int) (o obsdane) {
	o = obsdane{id:nastId("obszar_dane"), stanowisko:st, obserwacja:maxZam["A"+w.obser], pole:maxZam["B"+w.poleobsz], 
	            nasyc_rozklad:maxZam["C"+w.nasycrozk], nasyc_typ:maxZam["D"+w.nasyctyp], gestosc_znal:w.gest }
	f32, ferr := stof(w.obszpow)
	if ferr != nil {
	    fmt.Println(ferr.Error())
	    return
	}
	o.powierzchnia = f32
	return
}

func (w wiersz) newTerdane(st int) (t terdane) {
	t  = terdane{id:nastId("teren_dane"), stanowisko:st, zabudowany:"N", uwagi:w.blizter}
	tt := strings.Split(w.doster, "")
	for i:=0; i < len(tt); i++ {
		switch tt[i] {
			case "S": t.sred_zabud = "T"
			case "Z": t.zabudowany = "T"
			case "1": t.las = "T"
			case "2": t.sad = "T"
			case "3": t.park = "T"
			case "4": t.pole_orne="T"
			case "5": t.laka = "T"
			case "6": t.prywatny="T"
			case "7": t.spoleczny="T"
			case "8": t.przemyslowy="T"
		}
	}
	return
}

func (w wiersz) newWniodane(st int) (x wniodane) {
	x = wniodane{id:nastId("wnioski"), stanowisko:st, wartosc:trim(w.wart), uwagi:trim(w.wniodod)}
	ts := strings.Split(w.wnio, "")
	for i:=0; i < len(ts); i++ {
		switch ts[i] {
			case "1": x.inwentaryzacja="T"
			case "2": x.interwencja="T"
			case "3": x.wykopaliska="T"
		}
	}
	return
}

func (w wiersz) newZagdane(st int) (z zagdane) {
	z = zagdane{id:nastId("zagrozenia"), stanowisko:st, uwagi:w.zaguw, wystepowanie:maxZam["E"+w.zagwys], czas:maxZam["F"+w.zagczas]}
	if strings.Contains(w.zagprzy,"L") {
	    z.przyczyna_ludzie = "T"
	}
	if strings.Contains(w.zagprzy,"N") {
	    z.przyczyna_natura = "T"
	}
	if strings.Contains(w.zaguz,"P") {
	    z.uzytkownik_prywatny = "T"
	}
	if strings.Contains(w.zaguz,"N") {
	    z.uzytkownik_spoleczny = "T"
	}
	return
}

func (w wiersz) newAktdane(st int) (a aktdane) {
    a = aktdane{id:nastId("aktualnosci"), stanowisko:st, magazyn:w.magazyn, nr_inwentarza:w.nrinw}
    return
}

func (w wiersz) newGledane(st int) (g gledane) {
    g = gledane{id:nastId("gleba_dane"), stanowisko:st, kamienistosc:maxZam["J"+w.kam], uwagi:w.glespec}
    ts := strings.Split(w.gleba, "")
    for i:=0; i < len(ts); i++ {
        switch ts[i] {
            case "1":g.luzna="T"
            case "2":g.zwiezla="T"
            case "3":g.torf_bag="T"
        }
    }
    return
}

func (w wiersz) newKardane(st int) (k kardane) {
    k = kardane{id:nastId("karty"), stanowisko:st, nazwa_lok:w.nazlok, dalsze_losy:w.losy, dzieje_badan:w.hisbad, literatura:w.liter, autorzy:w.autor, chronologia:w.chrono, konsultant:w.konsul, arkusz_mapy:w.godlo, metryka_hist:w.zrodla}
    return
}

func NewFakt(tabs []string) (fw fkwiersz) {
    fw = fkwiersz{fun:trim(tabs[1]), kul:trim(tabs[2]), chro:trim(tabs[3]), mas:trim(tabs[4]), wydz:trim(tabs[5]), azp:trim(tabs[6])}
    return
}

type stazp struct {
    ob, nob string
}

func initFakty(plik string) map[stazp][]fkwiersz {
    var fm = make(map[stazp][]fkwiersz)
    pc, e := NewCsv(plik)
    if e != nil {
        panic(e.Error())
    }
    c := 0
    for {
        nt, nx := pc.Wiersz()
        if !nx {
            break
        }
        if c > 0 {
            nf := NewFakt(nt) 
            sa := stazp{ob:trim(nf.azp[:5]), nob:trim(nf.azp[5:])}
            fm[sa] = append(fm[sa],nf)
        }
        c+=1
    }
    return fm
}

func prepInfo(info string, rel bool) (pi []interface{}) {
    pi = make([]interface{},4)
    x := trim(strings.Replace(info,"*"," ",-1))
    pi[3] = 1.0
    if strings.Contains(x,"?") {
        x = trim(strings.Replace(x,"?"," ",-1))
        pi[3] = 0.5
    }
    if x == "" {
        pi[3]=0.0
    }
    if rel {
        var stab []string
        var re string
        if strings.Contains(x,"-") {
            stab = strings.Split(x,"-")
            re = "Z"
        } else if strings.Contains(x,"/") {
            stab = strings.Split(x,"/")
            re = "P"
        } else {
            stab = []string{x,""}
            re = ""
        }
        pi[0] = stab[0]
        pi[1] = stab[1]
        pi[2] = re
    } else {
        pi[0] = x
    }
    return
}

func dekodfk(f fkwiersz) (nf fkdane) {
    nf = fkdane{}
    pf := prepInfo(f.fun, false)
    nf.fun_pewnosc = float32(pf[3].(float64))
    nf.funkcja = pf[0].(string)
    
    pj := prepInfo(f.kul,true)
    nf.jeda = pj[0].(string)
    nf.jedb = pj[1].(string)
    nf.jed_relacja = pj[2].(string)
    nf.jed_pewnosc = float32(pj[3].(float64))
    
    po := prepInfo(f.chro,true)
    nf.okresa = po[0].(string)
    nf.okresb = po[1].(string)
    nf.okr_relacja = po[2].(string)
    nf.okr_pewnosc = float32(po[3].(float64)) 
    nf.masowy = trim(f.mas)
    nf.wydzielony = trim(f.wydz)
    return
}

func dodajFakty(fk []fkwiersz, st int) {
    for i:=0; i < len(fk); i++ {
        fd := dekodfk(fk[i])
        fd.id = nastId("fakty")
        fd.stanowisko = st
        dodaj(fkps,fd,false)
    }
    fmt.Print(len(fk),", ")
}

func init() {
    flag.Usage = func() {
        fmt.Fprintf(os.Stderr, "Aby uruchomić program %s należy wszyskie parametry podane poniżej:\n", os.Args[0])
        fmt.Fprintln(os.Stderr, "  -f nazwa_pliku : plik csv z informacjami o faktach kulturowych z azpmax")
        fmt.Fprintln(os.Stderr, "  -s nazwa_pliku : plik csv z informacjami o stanowiskach z azpmax")
        fmt.Fprintln(os.Stderr, "  -c nazwa_pliku : plik docelowej bazy")
        fmt.Fprintln(os.Stderr, "  -w nazwa_pliku : plik bazy ze wspólrzędnymi")
        
    }
    flag.StringVar(&faktyPlik, "f", "","plik csv z informacjami o faktach kulturowych z azpmax")
    flag.StringVar(&stPlik, "s", "", "plik csv z informacjami o stanowiskach z azpmax")
    flag.StringVar(&bazaPlik, "c", "", "baza docelowa")
    flag.StringVar(&wspPlik, "w", "", "baza ze wspolrzednymi")
}

func main2() {
    flag.Parse()
    fmt.Println("w: ",faktyPlik, stPlik, bazaPlik, wspPlik, flag.Parsed())
}

func main() {
    flag.Parse()
    if flag.NFlag() < 4 {
        flag.Usage()
        return
    }
    c := 0
    ie := initDb(wspPlik, bazaPlik)
    ie = initStmt()
    if ie != nil {
        fmt.Println(ie.Error())
    }
    mwyk, ie = initWykaz("miejscowosci")
    if ie != nil {
        fmt.Println(ie.Error())
    }
    gwyk, ie = initWykaz("gminy")
    if ie != nil {
        fmt.Println(ie.Error())
    }
    pwyk, ie = initWykaz("powiaty")
    if ie != nil {
        fmt.Println(ie.Error())
    }
    wwyk, ie = initWykaz("wojewodztwa")
    if ie != nil {
        fmt.Println(ie.Error())
    }    
    fakty := initFakty(faktyPlik)
    dcsv, e := NewCsv(stPlik)
    if e != nil {
        fmt.Println(e.Error())
    } else {
        for {
            nt, nx := dcsv.Wiersz()
            if !nx {
                break
            } 
            nw := NewWiersz(nt) 
            if c > 0 {
                if st, err := nw.newStanowisko(); err == nil {
                    si := stazp{ob:st.obszar, nob:nobs(st.nrObszar)}
                    if ft, ok := fakty[si]; !ok {
                        c+=1
                        continue 
                    } else {
                        dodaj(stps, st, false)
                        dodajFakty(ft,st.id)
                    }   
                    dodaj(fgps, nw.newFizgeo(st.id), true)
                    dodaj(ekps, nw.newEksdane(st.id), true)   
                    dodaj(obps, nw.newObsdane(st.id), true)
                    dodaj(teps, nw.newTerdane(st.id), true)
                    dodaj(wnps, nw.newWniodane(st.id), true)
                    dodaj(zaps, nw.newZagdane(st.id), true)      
                    dodaj(akps, nw.newAktdane(st.id), true)
                    dodaj(gbps, nw.newGledane(st.id), true)
                    dodaj(kaps, nw.newKardane(st.id), true)  
                } else {
                    fmt.Println(err.Error())
                }
            }
            c+=1
        }
    }
    fmt.Println("Odczytano:",c)
    wspDb.Close()
    azpDb.Close()
}

