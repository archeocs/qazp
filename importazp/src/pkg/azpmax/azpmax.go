package main

import (
  //  "io"
    "os"
    "bufio"
    "strings"
    "fmt"
    "strconv"
  //  "database/sql"
    "math"
    )

/**/

func NewCsv(sciezka string) (dane *csv, err error) {
    dane = new(csv)
    if dane.plik, err = os.Open(sciezka); err != nil {
        return
    }
    dane.rd = bufio.NewReader(dane.plik)
    return
}


func (dane *csv) Nastepny() (tabs []string, next bool) {
    var (
        linia string
        re error
    )
    if linia, re = dane.rd.ReadString('\n'); re != nil {
        dane.plik.Close()
        next = false
        fmt.Println(re.Error())
        return
        // return nil, false
    }
    tabs = strings.Split(linia, "#")
    next = true
    return
}

func NewWiersz(tabs []string) (cw wiersz) {
    cw = wiersz{miej:trim(tabs[0]), gm:trim(tabs[1]), woj:trim(tabs[2]), obsz:trim(tabs[5]), nrobsz:trim(tabs[7]), nrmiej:trim(tabs[6]), nazlok:trim(tabs[9]), rodzbad:trim(tabs[10]), databad:trim(tabs[38]), autor:trim(tabs[39]), region:trim(tabs[12]), jedfiz:trim(tabs[13]), rodzeks:trim(tabs[14]), wyseks:trim(tabs[16]), kiereks:trim(tabs[18]), stopeks:trim(tabs[17]), forszczeg:trim(tabs[15]), doster:trim(tabs[22]), blizter:trim(tabs[23]), obser:trim(tabs[24]), poleobsz:trim(tabs[25]), nasycrozk:trim(tabs[26]), nasyctyp:trim(tabs[27]), obszpow:trim(tabs[28]), gest:trim(tabs[29]), zagwys:trim(tabs[30]), zagczas:trim(tabs[31]), zagprzy:trim(tabs[32]), zaguz:trim(tabs[33]), zaguw:trim(tabs[34]), wart:trim(tabs[35]), wnio:trim(tabs[36]), wniodod:trim(tabs[37]), chrono:trim(tabs[40]), konsul:trim(tabs[41]), magazyn:trim(tabs[42]), losy:trim(tabs[43]), hisbad:trim(tabs[44]), nrinw:trim(tabs[11]), liter:trim(tabs[45]), godlo:trim(tabs[46]), uwagi:trim(tabs[50]), gleba:trim(tabs[19]), kam:trim(tabs[20]), glespec:trim(tabs[21]), zrodla:trim(tabs[49])}
    return
}

func trim(s string) string {
    return strings.TrimSpace(s)
}

func dekodrodz(r string) string {
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

func stwsp(ob, nrob string) (geom string) {
    r := geops.QueryRow(ob, nrob)
    r.Scan(&geom)
    return
}

func tb(s string) []byte {
    return []byte(s)
}

func (w wiersz) genst() (st stanowisko) {
    st = stanowisko{obszar:w.obsz, nrObszar:w.nrobsz, miejscowosc:mwyk.ident(w.miej), 
                        gmina:gwyk.ident(w.gm), powiat: pwyk.ident(w.powiat), 
                        wojewodztwo:wwyk.ident(w.woj), rodzBad:dekodrodz(w.rodzbad),
                        autor:w.autor, data:w.databad, nrMiej:w.nrmiej, id:nastId("stanowiska"), uwagi:w.uwagi}
    st.geom = stwsp(st.obszar, st.nrObszar)
    return
}

func (w wiersz) genEkspo(st int) (e eksdane) {
    e = eksdane{ stanowisko:st, id:nastId("ekspozycja_dane"), uwagi:w.forszczeg}
    rodzEks(w.rodzeks, &e)
    rozmEks(w.wyseks, &e)
    stopEks(w.stopeks, &e)
    kierEks(w.kiereks, &e)
    return
}

func kierEks(d string, e *eksdane) bool {
   // fmt.Println("kierunek ",d)
    var kiers = map[string]float64 {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}
    td := strings.Split(d, "")
    dkier := 0.0
    for i:=0; i < len(td); i++ {
        dkier += math.Pow(2,kiers[td[i]])
    }
    e.kierunek = int(dkier)
    return true
}

func stopEks(d string, e *eksdane) bool {
// fmt.Println("stop ",d)
    switch d {
        case "1": e.stopien = 0.5
        case "2": e.stopien = 2
        case "3": e.stopien = 5.5
        case "4": e.stopien = 11.5
        case "5": e.stopien = 16
        default: e.stopien = 0
    }
    return true
}

func rozmEks(d string, e *eksdane) bool {
   // fmt.Println("rozm ",d)
    if d == "" {
        return true
    }
    v, er := strconv.ParseFloat(d, 32)
    if er != nil {
        fmt.Println(er.Error())
        return false
    }
    e.rozmiar = float32(v)
    return true
}

func rodzEks(d string, e *eksdane) bool {
    // fmt.Println("rodz ",d)
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
    return true
}

func (w wiersz) genFizgeo(st int) (f fizgeo) {
    f = fizgeo{uwagi:w.region, stanowisko:st, id:nastId("fizgeo_dane")}
    tj := strings.Split(w.jedfiz, "")
    //fmt.Println(w.jedfiz, tj)
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

var (
	mb = map[string]string {"A0":"U", "A1":"B", "A":"", "B0":"O", "B1":"Z", "B":"", "C0":"R", "C1":"N", "C":"", "D0":"J", "D1":"W", "D2":"D", "D":"", "E1":"I", "E0":"N", "E":"", "F0":"D", "F1":"S", "F":"", "GL":"L", "GN":"N", "G":"", "HP":"P", "HS":"S", "H":"", "JM":"M", "JS":"S", "JD":"D", "J":""}
)

func stof(s string) float32 {
    if s == "" {
        return 0
    }
    f, e := strconv.ParseFloat(s, 32)
    if e != nil {
        panic(e.Error())
    }
    return float32(f)
}

func (w wiersz) genObszar(st int) (o obsdane) {
	o = obsdane{id:nastId("obszar_dane"), stanowisko:st, powierzchnia:stof(w.obszpow), obserwacja:mb["A"+w.obser],
				pole:mb["B"+w.poleobsz], nasyc_rozklad:mb["C"+w.nasycrozk], nasyc_typ:mb["D"+w.nasyctyp], gestosc_znal:w.gest }
	return
}

func (w wiersz) genTer(st int) (t terdane) {
	t  = terdane{id:nastId("teren_dane"), stanowisko:st, zabudowany:"N", uwagi:w.blizter}
	dekodTer(w.doster, &t)
	return
}

func dekodTer(ter string, t *terdane) bool {
	tt := strings.Split(ter, "")
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
	return true
}

func (w wiersz) genWnio(st int) (x wniodane) {
	x = wniodane{id:nastId("wnioski"), stanowisko:st, wartosc:trim(w.wart), uwagi:trim(w.wniodod)}
	dekodWnio(w.wnio, &x)
	return
}

func dekodWnio(wn string, w *wniodane) bool {
    ts := strings.Split(wn, "")
	for i:=0; i < len(ts); i++ {
		switch ts[i] {
			case "1": w.inwentaryzacja="T"
			case "2": w.interwencja="T"
			case "3": w.wykopaliska="T"
		}
	}
	return true
}

func (w wiersz) genZagr(st int) (z zagdane) {
	z = zagdane{id:nastId("zagrozenia"), stanowisko:st, uwagi:w.zaguw, wystepowanie:mb["E"+w.zagwys], czas:mb["F"+w.zagczas]}
	// przyczyna:mb["G"+w.zagprzy], uzytkownik:mb["H"+w.zaguz]} // sprawdz azpmax
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

func (w wiersz) genAkt(st int) (a aktdane) {
    a = aktdane{id:nastId("aktualnosci"), stanowisko:st, magazyn:w.magazyn, nr_inwentarza:w.nrinw}
    return
}

func (w wiersz) genGleb(st int) (g gledane) {
    g = gledane{id:nastId("gleba_dane"), stanowisko:st, kamienistosc:mb["J"+w.kam], uwagi:w.glespec}
    dekodGleba(w.gleba, &g)
    return
}

func dekodGleba(gleba string, g *gledane) {
    ts := strings.Split(gleba, "")
    for i:=0; i < len(ts); i++ {
        switch ts[i] {
            case "1":g.luzna="T"
            case "2":g.zwiezla="T"
            case "3":g.torf_bag="T"
        }
    }
}

func (w wiersz) genKarta(st int) (k kardane) {
    k = kardane{id:nastId("karty"), stanowisko:st, nazwa_lok:w.nazlok, dalsze_losy:w.losy, dzieje_badan:w.hisbad, literatura:w.liter, autorzy:w.autor, chronologia:w.chrono, konsultant:w.konsul, arkusz_mapy:w.godlo, metryka_hist:w.zrodla}
    return
}

func NewFakt(tabs []string) (fw fkwiersz) {
    // fmt.Println(len(tabs))
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
        nt, nx := pc.Nastepny()
        if !nx {
            break
        }
        if c > 0 {
            nf := NewFakt(nt) 
            sa := stazp{ob:trim(nf.azp[:5]), nob:trim(nf.azp[5:])}
            fm[sa] = append(fm[sa],nf)
        }
        c+=1
        //ob := trim(nf.azp[:5])
        //nob := trim(nf.azp[5:])
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

/*
String ns = ss.replace('*', ' ').replace(' ', ' ').trim();
		if (ns.startsWith("?") || ns.endsWith("?")) {
			epew = 0.5;
			ns = ns.replace('?', ' ').trim();
		}
		ns = ns.replace('?', ' ').trim();
		if (ns.isEmpty()) {
			epew = 0;
			return;
		}
		if (ns.contains("-")) {
			String[] ab = ns.split("-");
			ep1 = ab[0];
			ep2 = ab[1];
			erel="Z";
			//System.out.println(this);
		}
		else if (ns.contains("/")) {
			String[] ab = ns.split("/");
			ep1 = ab[0];
			ep2 = ab[1];
			erel="P";
			//System.out.println(this);
		} else
			ep1 = ns;*/

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

func main() {
    c := 0
    ie := initDb("pierwsze.db", "azp2.db")
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
    fakty := initFakty("/home/milosz/archeocs/import_azpmax/pierwsze_csv/wszy2.csv")
    dcsv, e := NewCsv("/home/milosz/archeocs/import_azpmax/pierwsze_csv/dane5127.csv")
    if e != nil {
        fmt.Println(e.Error())
    } else {
        for {
            nt, nx := dcsv.Nastepny()
            if !nx {
                break
            } 
            nw := NewWiersz(nt) 
            if c > 0 {
//                st := nw.genst()
//                e = dodaj(st,false)
//                f := nw.genFizgeo(st.id)
                st := nw.genst()
                si := stazp{ob:st.obszar, nob:nobs(st.nrObszar)}
                e := nw.genEkspo(st.id)
                f := nw.genFizgeo(st.id)
                o := nw.genObszar(st.id)
                t := nw.genTer(st.id)
                w := nw.genWnio(st.id)
                z := nw.genZagr(st.id)
                a := nw.genAkt(st.id)
                g := nw.genGleb(st.id)
                k := nw.genKarta(st.id)
                dodaj(stps, st,false)
                dodaj(fgps, f,true)
                dodaj(ekps, e,true)   
                dodaj(obps, o,true)
                dodaj(teps, t,true)
                dodaj(wnps, w,true)
                dodaj(zaps, z,true)      
                dodaj(akps, a, true)
                dodaj(gbps, g, true)
                dodaj(kaps, k, true)  
                if ft, ok := fakty[si]; !ok {
                    fmt.Printf("%#v\n",si)
                    panic("brak faktow")
                } else {
                    dodajFakty(ft,st.id)
                }     
                if c % 10 == 0 {
                    fmt.Println(c)
                    // fmt.Printf("%#v\n\n",st)
                    fmt.Printf("%#v\n\n",e)
                    fmt.Printf("%#v\n\n",f)
                    fmt.Printf("%#v\n\n",o)
                    fmt.Printf("%#v\n\n",t)
                    fmt.Printf("%#v\n\n",w)
                    fmt.Printf("%#v\n\n",z)
                    fmt.Printf("%#v\n\n",a)
                    fmt.Printf("%#v\n\n",g)
                    fmt.Printf("%#v\n\n",k)
                    fmt.Printf("%#v\n\n",nw)
                    fmt.Printf("%#v\n\n",fakty[si])
                }
            }
            c+=1
        }
    }
    fmt.Println("Odczytano:",c)
    wspDb.Close()
    azpDb.Close()
}

