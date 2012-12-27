package main

import (
    "os"
    "bufio"
    "fmt"
    "strconv"
)

type Tabela interface {
	Params() []interface{}
}

type wiersz struct {
    miej string
    gm string
    woj string
    powiat string
    obsz string
    nrobsz string
    nrmiej string
    nazlok string
    rodzbad string
    nrinw string
    region string
    jedfiz string
    rodzeks string
    forszczeg string
    wyseks string
    stopeks string
    kiereks string
    gleba string
    kam string // kamienistosc
    glespec string // okr specjalistyczne
    doster string // dost terenu
    blizter string // teren - okr blizsze
    obser string // obserwacja utrudniona /bezp
    poleobsz string // pole (otwar
    nasycrozk string // nasycenie znal (rownomierne, niero)
    nasyctyp string // nasycenie typ (jedno, wielo)
    obszpow string // powierzchnia
    gest string // gestosc (mala, sre)
    zagwys string // wystepowanie
    zagczas string // dorazne ..
    zagprzy string // przyczyna
    zaguz string // uzytkownik
    zaguw string // uwagi
    wart string // wnioski wartosc
    wnio string // wnioski
    wniodod string // dane dodatkowe
    databad string 
    autor string 
    chrono string
    konsul string
    magazyn string
    losy string
    hisbad string // historia badan
    liter string // literatura
    godlo string // godlo mapy
    zrodla string // metryka historyczna
    uwagi string
}

type fkwiersz struct {
    kul string
    chro string
    fun string
    mas string
    wydz string
    azp string
}

func nilstr(s string) interface{} {
    if s == "" {
        return nil
    }
    return s
}

func nili(n int) interface{} {
    if n == 0 {
        return nil
    }
    return n
}

func nilf(n float32) interface{} {
    if n == 0 {
        return nil
    }
    return n
}

func nobs(s string) string {
    v, e := strconv.ParseFloat(trim(s),32)
    //fmt.Println(v, strconv.Itoa(int(v)))
    if e != nil {
        fmt.Println(e.Error())
    }
    return strconv.Itoa(int(v))
}

type stanowisko struct {
    id int
    obszar string
    nrObszar string
    miejscowosc int
    nrMiej string
    gmina int
    powiat int
    wojewodztwo int
    geom string
    rodzBad string
    autor string
    data string
    uwagi string
}


func (s stanowisko) Params() []interface{} {
    return []interface{} {s.id, s.obszar, nobs(s.nrObszar), s.miejscowosc, s.nrMiej, nili(s.gmina), nili(s.powiat), nili(s.wojewodztwo),
                            nilstr(s.data), nilstr(s.autor), nilstr(s.rodzBad), nilstr(s.uwagi), s.geom}
}

type fizgeo struct {
    id int
    stanowisko int // integer not null,
    nadmorska string //varchar(1) check (nadmorska in ('T','N')),
    w_morzu string //varchar(1) check (w_morzu in ('T','N')),
    plaza string //varchar(1) check (plaza in ('T','N')),
    mierzeja string //varchar(1) check (mierzeja in ('T','N')),
    skarpa string //varchar(1) check (skarpa in ('T','N')),
    wal_wydmowy string //varchar(1) check (wal_wydmowy in ('T','N')),
    duze_doliny string //varchar(1) check (duze_doliny in ('T','N')),
    w_wodzie string //varchar(1) check (w_wodzie in ('T','N')),
    ter_denna string //varchar(1) check (ter_denna in ('T','N')),
    ter_nadzalewowa string //varchar(1) check (ter_nadzalewowa in ('T','N')),
    ter_wyzsze string //varchar(1) check (ter_wyzsze in ('T','N')),
    brzeg_wysoczyzny string //varchar(1) check (brzeg_wysoczyzny in ('T','N')),
    male_doliny string //varchar(1) check (male_doliny in ('T','N')),
    dno_doliny string //varchar(1) check (dno_doliny in ('T','N')),
    stok_doliny string //varchar(1) check (stok_doliny in ('T','N')),
    krawedz_doliny string //varchar(1) check (krawedz_doliny in ('T','N')),
    poza_dolinami string //varchar(1) check (poza_dolinami in ('T','N')),
    rownina string //varchar(1) check (rownina in ('T','N')),
    obsz_falisty string //varchar(1) check (obsz_falisty in ('T','N')),
    obsz_pagorkowaty string //varchar(1) check (obsz_pagorkowaty in ('T','N')),
    obsz_gorzysty string //varchar(1) check (obsz_gorzysty in ('T','N')),
    uwagi string //varchar(255)
}

func (fg fizgeo) Params() []interface{} {
    return []interface{} {fg.id, fg.stanowisko, nilstr(fg.nadmorska), nilstr(fg.w_morzu), nilstr(fg.plaza), nilstr(fg.mierzeja), 
                                nilstr(fg.skarpa), nilstr(fg.wal_wydmowy), nilstr(fg.duze_doliny), nilstr(fg.w_wodzie), 
                                nilstr(fg.ter_denna), nilstr(fg.ter_nadzalewowa), nilstr(fg.ter_wyzsze), nilstr(fg.brzeg_wysoczyzny),
                                 nilstr(fg.male_doliny), nilstr(fg.dno_doliny), nilstr(fg.stok_doliny), nilstr(fg.krawedz_doliny),
                                 nilstr(fg.poza_dolinami), nilstr(fg.rownina), nilstr(fg.obsz_falisty), nilstr(fg.obsz_pagorkowaty), 
                                 nilstr(fg.obsz_gorzysty),nilstr(fg.uwagi)}
}

type eksdane struct {
    id int // not null,
    stanowisko int // not null,
    eksponowany string // varchar(1) check (eksponowany in ('T','N')),
    kraw_stoki string // varchar(1) check (kraw_stoki in ('T','N')),
    sfaldowania_cyple string // varchar(1) check (sfaldowania_cyple in ('T','N')),
    cyple_wybitne string // varchar(1) check (cyple_wybitne in ('T','N')),
    waly_garby string // varchar(1) check (waly_garby in ('T','N')),
    wyniesienia_okrezne string // varchar(1) check (wyniesienia_okrezne in ('T','N')),
    osloniety string // varchar(1) check (osloniety in ('T','N')),
    podst_stoku string // varchar(1) check (podst_stoku in ('T','N')),
    doliny_niecki string // varchar(1) check (doliny_niecki in ('T','N')),
    kotlinki_zagleb string // varchar(1) check (kotlinki_zagleb in ('T','N')),
    jaskinie string // varchar(1) check (jaskinie in ('T','N')),
    rozmiar float32 //string // decimal(4,1),
    stopien float32 //string // decimal(3,1),
    kierunek int // integer check (kierunek between 0 and 256),
    uwagi string //z varchar(255),
}

func (ek eksdane) Params() []interface{} {
    return []interface{} {ek.id, ek.stanowisko, nilstr(ek.eksponowany), nilstr(ek.kraw_stoki), nilstr(ek.sfaldowania_cyple),
                                nilstr(ek.cyple_wybitne), nilstr(ek.waly_garby), nilstr(ek.wyniesienia_okrezne),
                                nilstr(ek.osloniety), nilstr(ek.podst_stoku), nilstr(ek.doliny_niecki), nilstr(ek.kotlinki_zagleb),
                                nilstr(ek.jaskinie), nilf(ek.rozmiar), nilf(ek.stopien), nili(ek.kierunek), nilstr(ek.uwagi)}
}

type obsdane struct {
	id int
    stanowisko int
    obserwacja string //varchar(1), -- utrudniona / bez przeszkod
    pole string // varchar(1), -- otwarte / zamkniete
    nasyc_rozklad string // varchar(1), -- rownomierny / nierownomierny
    nasyc_typ string // string varchar(1), -- jednocentryczne / wielocentryczne / dekocentryczne
    powierzchnia float32 // decimal(9,2),
    gestosc_znal string // varchar(1), -- mala / srednia /duza
    uwagi string // varchar(255),
}

func (o obsdane) Params() []interface{} {
	return []interface{} {o.id, o.stanowisko, nilstr(o.obserwacja), nilstr(o.pole), nilstr(o.nasyc_rozklad), nilstr(o.nasyc_typ), nilf(o.powierzchnia), nilstr(o.gestosc_znal), nilstr(o.uwagi)}
}

type terdane struct {
	id int //integer not null,
    stanowisko int //integer not null,
    zabudowany string // varchar(1) check (zabudowany in ('T','N')),
    sred_zabud string //  varchar(1) check (sred_zabud in ('T','N')),
    las string //  varchar(1) check (las in ('T','N')),
    sad string //  varchar(1) check (sad in ('T','N')),
    park string //  varchar(1) check (park in ('T','N')),
    pole_orne string //  varchar(1) check (pole_orne in ('T','N')),
    laka string //  varchar(1) check (laka in ('T','N')),
    nieuzytek string //  varchar(1) check (nieuzytek in ('T','N')),
    torf string //  varchar(1) check (torf in ('T','N')),
    woda string //  varchar(1) check (woda in ('T','N')),
    bagno string //  varchar(1) check (bagno in ('T','N')), 
    prywatny string //  varchar(1) check (prywatny in ('T','N')),
    spoleczny string //  varchar(1) check (spoleczny in ('T','N')),
    przemyslowy string //  varchar(1) check (przemyslowy in ('T','N')),
    uwagi string //  varchar(255), 
}

func (t terdane) Params() []interface{} {
	return []interface{}{t.id, t.stanowisko, nilstr(t.zabudowany), nilstr(t.sred_zabud), nilstr(t.las), nilstr(t.sad), nilstr(t.park), nilstr(t.pole_orne), nilstr(t.laka), nilstr(t.prywatny), nilstr(t.spoleczny), nilstr(t.przemyslowy), nilstr(t.uwagi)}
}

type wniodane struct {
	id int //integer not null,
    stanowisko int //integer not null,
    wartosc string //varchar(1), -- mala / srednia / duza
    inwentaryzacja string //varchar(1) check (inwentaryzacja in ('T','N')),
    wykopaliska string //varchar(1) check (wykopaliska in ('T','N')),
    interwencja string //varchar(1) check (interwencja in ('T','N')),
    uwagi string //varchar(255)
}

func (w wniodane) Params() []interface{} {
	return []interface{} {w.id, w.stanowisko, nilstr(w.wartosc), nilstr(w.inwentaryzacja), nilstr(w.wykopaliska), nilstr(w.interwencja), nilstr(w.uwagi)}
}

type zagdane struct {
	id int // integer not null,
    stanowisko int // integer not null,
    wystepowanie string //varchar(1) not null, -- istnieje / nie istnieje
    czas string //varchar(1), -- stale / dorazne
    przyczyna_ludzie string //varchar(1) check (przyczyna_ludzie in ('T','N')),
    przyczyna_natura string //varchar(1) check (przyczyna_natura in ('T','N')),
    uzytkownik_spoleczny string // varchar(1) check (uzytkownik_spoleczny in ('T','N')),
    uzytkownik_prywatny string //varchar(1) check (uzytkownik_prywatny in ('T','N')),
    //przyczyna string //varchar(1), -- ludzie / natura
    // uzytkownik string //varchar(1), -- wypelniane jezeli przyczyna == ludzie: uzytkownik spoleczny / prywatny
    uwagi string //varchar(255),
}

func (z zagdane) Params() []interface{} {
	return []interface{} {z.id, z.stanowisko, nilstr(z.wystepowanie), nilstr(z.czas), nilstr(z.przyczyna_ludzie), nilstr(z.przyczyna_natura), nilstr(z.uzytkownik_spoleczny), nilstr(z.uzytkownik_prywatny), nilstr(z.uwagi)}
}

type aktdane struct {
  id int // integer NOT NULL,
  stanowisko int // integer NOT NULL,
  magazyn string // varchar(20),
  nr_inwentarza string // varchar(20),
  nr_krz string //  varchar(20), -- nr rejestru zabytkow
  data_krz string //  date, -- data wpisu do rejestru
  par string // k character varying(20), -- park kulturowy
  plan string //  character varying(50),
  wlasciciel string //  varchar(500),
  uwagi string //  varchar(255),
}

func (a aktdane) Params() []interface{} {
    return []interface{} {a.id, a.stanowisko, nilstr(a.magazyn), nilstr(a.nr_inwentarza)}
}

type gledane struct {
  id int // integer NOT NULL,
  stanowisko int // integer NOT NULL,
  luzna string // character varying(1) check (luzna in ('T','N')),
  zwiezla string //character varying(1) check (zwiezla in ('T','N')),
  torf_bag string //character varying(1) check (torf_bag in ('T','N')),
  kamienistosc string //character varying(1) check (kamienistosc in ('M','S','D')),
  uwagi string //character varying(255),
}

func (g gledane) Params() []interface{} {
    return []interface{} {g.id, g.stanowisko, nilstr(g.luzna), nilstr(g.zwiezla), nilstr(g.torf_bag), nilstr(g.kamienistosc), nilstr(g.uwagi)}
}

type kardane struct {
  id int //integer not null,
  stanowisko int // integer NOT NULL,
  nazwa_lok string // varchar(50),
  arkusz_mapy string // varchar(10),
  dalsze_losy string // varchar(100),
  dzieje_badan string // varchar(100),
  metryka_hist string // varchar(10),
  literatura string // varchar(100),
  dzialka_geodezyjna string // varchar(255),
  egb string // character varying(500) ,
  autorzy string // character varying(255),
  chronologia string // character varying(255), -- okreslil chronologie
  konsultant string // character varying(255), -- sprawdzil
  uwagi string // varchar(255),
}

func (k kardane) Params() []interface{} {
    return []interface{} {k.id, k.stanowisko, nilstr(k.nazwa_lok), nilstr(k.arkusz_mapy), nilstr(k.dalsze_losy), nilstr(k.dzieje_badan), nilstr(k.literatura), nilstr(k.autorzy), nilstr(k.chronologia), nilstr(k.konsultant)}
}

type fkdane struct {
    id int //integer, 
    stanowisko int // integer, 
    okresa string //varchar(2),
    okresb string // varchar(2),
    okr_relacja string // varchar(1) check (okr_relacja in ('Z','P')),
    okr_pewnosc float32 // decimal(3,2),
    jeda string // varchar(6), 
    jedb string // varchar(6), 
    jed_relacja string // varchar(1) check (jed_relacja in ('Z','P')), 
    jed_pewnosc float32 // decimal(3,2), 
    funkcja string // varchar(8), 
    fun_pewnosc float32 // decimal(3,2), 
    masowy string // varchar(50), 
    wydzielony string // varchar(50),
}

func (f fkdane) Params() []interface{} {
    return []interface{} {f.id, f.stanowisko, nilstr(f.okresa), nilstr(f.okresb), nilstr(f.okr_relacja), nilf(f.okr_pewnosc),
    nilstr(f.jeda), nilstr(f.jedb), nilstr(f.jed_relacja), nilf(f.jed_pewnosc), nilstr(f.funkcja), nilf(f.fun_pewnosc), nilstr(f.masowy), nilstr(f.wydzielony) }
}

type csv struct {
    plik *os.File
    rd *bufio.Reader
}

type wykaz struct {
    mapa map[string]int
    ostatni int
    nazwa string
}
