CREATE TABLE EKSPOZYCJA_DANE(
    id integer not null,
    stanowisko integer not null,
    eksponowany varchar(1) check (eksponowany in ('T','N')),
    kraw_stoki varchar(1) check (kraw_stoki in ('T','N')),
    sfaldowania_cyple varchar(1) check (sfaldowania_cyple in ('T','N')),
    cyple_wybitne varchar(1) check (cyple_wybitne in ('T','N')),
    waly_garby varchar(1) check (waly_garby in ('T','N')),
    wyniesienia_okrezne varchar(1) check (wyniesienia_okrezne in ('T','N')),
    osloniety varchar(1) check (osloniety in ('T','N')),
    podst_stoku varchar(1) check (podst_stoku in ('T','N')),
    doliny_niecki varchar(1) check (doliny_niecki in ('T','N')),
    kotlinki_zagleb varchar(1) check (kotlinki_zagleb in ('T','N')),
    jaskinie varchar(1) check (jaskinie in ('T','N')),
    rozmiar decimal(4,1),
    stopien decimal(3,1),
    kierunek integer check (kierunek between 0 and 256),
    uwagi varchar(255),
    CONSTRAINT kspozycja_dane_pkey PRIMARY KEY (id),
    constraint unique_ekspozycja_dane_st unique(id, stanowisko)
    
);
CREATE TABLE FIZGEO_DANE(
    id integer not null,
    stanowisko integer not null,
    nadmorska varchar(1) check (nadmorska in ('T','N')),
    w_morzu varchar(1) check (w_morzu in ('T','N')),
    plaza varchar(1) check (plaza in ('T','N')),
    mierzeja varchar(1) check (mierzeja in ('T','N')),
    skarpa varchar(1) check (skarpa in ('T','N')),
    wal_wydmowy varchar(1) check (wal_wydmowy in ('T','N')),
    duze_doliny varchar(1) check (duze_doliny in ('T','N')),
    w_wodzie varchar(1) check (w_wodzie in ('T','N')),
    ter_denna varchar(1) check (ter_denna in ('T','N')),
    ter_nadzalewowa varchar(1) check (ter_nadzalewowa in ('T','N')),
    ter_wyzsze varchar(1) check (ter_wyzsze in ('T','N')),
    brzeg_wysoczyzny varchar(1) check (brzeg_wysoczyzny in ('T','N')),
    male_doliny varchar(1) check (male_doliny in ('T','N')),
    dno_doliny varchar(1) check (dno_doliny in ('T','N')),
    stok_doliny varchar(1) check (stok_doliny in ('T','N')),
    krawedz_doliny varchar(1) check (krawedz_doliny in ('T','N')),
    poza_dolinami varchar(1) check (poza_dolinami in ('T','N')),
    rownina varchar(1) check (rownina in ('T','N')),
    obsz_falisty varchar(1) check (obsz_falisty in ('T','N')),
    obsz_pagorkowaty varchar(1) check (obsz_pagorkowaty in ('T','N')),
    obsz_gorzysty varchar(1) check (obsz_gorzysty in ('T','N')),
    uwagi varchar(255),
    CONSTRAINT fizgeo_dane_pkey PRIMARY KEY (id),
    constraint unique_fizgeo_dane_st unique(id, stanowisko)
);
CREATE TABLE OBSZAR_DANE(
    id integer not null,
    stanowisko integer not null,
    obserwacja varchar(1), -- utrudniona / bez przeszkod
    pole varchar(1), -- otwarte / zamkniete
    nasyc_rozklad varchar(1), -- rownomierny / nierownomierny
    nasyc_typ varchar(1), -- jednocentryczne / wielocentryczne / dekocentryczne
    powierzchnia decimal(9,2),
    gestosc_znal varchar(1), -- mala / srednia /duza
    uwagi varchar(255),
    CONSTRAINT obszar_dane_pkey PRIMARY KEY (id),
    CONSTRAINT check_obserwacja CHECK (obserwacja in ('U','B')),
    CONSTRAINT check_pole CHECK (pole in ('O','Z')),
    CONSTRAINT check_nasyc_rozklad CHECK (nasyc_rozklad in ('R','N')),
    CONSTRAINT check_nasyc_typ CHECK (nasyc_typ in ('J','W','D')),
    CONSTRAINT check_gestosc_znal CHECK (gestosc_znal in ('M','S','D')),
    constraint unique_obszar_dane_st unique(id, stanowisko)
);
CREATE TABLE STANOWISKA(
    id integer not null,
    obszar varchar(8) not null,
    nr_obszar varchar(5) not null,
    miejscowosc integer null default -1,
    nr_miejscowosc varchar(5) null default '',
    gmina integer null default -1,
    powiat integer null default -1,
    wojewodztwo integer null default -1,
    rodzaj_badan varchar(1) not null default '?',
    data varchar(10),
    autor varchar(20),
    uwagi varchar(255),
    powierzchnia varchar(2),
    etykieta_x varchar(20),
    etykieta_y varchar(20),
    etykieta_kolor varchar(7),
    wspolrzedne POLYGON,
    constraint stanowiska_pkey primary key(id)
);
CREATE VIRTUAL TABLE SpatialIndex USING VirtualSpatialIndex();
CREATE TABLE TEREN_DANE(
    id integer not null,
    stanowisko integer not null,
    zabudowany varchar(1) check (zabudowany in ('T','N')),
    sred_zabud varchar(1) check (sred_zabud in ('T','N')),
    las varchar(1) check (las in ('T','N')),
    sad varchar(1) check (sad in ('T','N')),
    park varchar(1) check (park in ('T','N')),
    pole_orne varchar(1) check (pole_orne in ('T','N')),
    laka varchar(1) check (laka in ('T','N')),
    nieuzytek varchar(1) check (nieuzytek in ('T','N')),
    torf varchar(1) check (torf in ('T','N')),
    woda varchar(1) check (woda in ('T','N')),
    bagno varchar(1) check (bagno in ('T','N')), 
    prywatny varchar(1) check (prywatny in ('T','N')),
    spoleczny varchar(1) check (spoleczny in ('T','N')),
    przemyslowy varchar(1) check (przemyslowy in ('T','N')),
    uwagi varchar(255), 
    CONSTRAINT teren_dane_pkey PRIMARY KEY (id),
      constraint unique_teren_dane_st unique(id, stanowisko)
);
CREATE TABLE WNIOSKI(
    id integer not null,
    stanowisko integer not null,
    wartosc varchar(1), -- mala / srednia / duza
    inwentaryzacja varchar(1) check (inwentaryzacja in ('T','N')),
    wykopaliska varchar(1) check (wykopaliska in ('T','N')),
    interwencja varchar(1) check (interwencja in ('T','N')),
    uwagi varchar(255),
    CONSTRAINT wnioski_pkey PRIMARY KEY (id),
    CONSTRAINT check_wartosc CHECK (wartosc in ('M','S','D')),
    constraint unique_wnioski_st unique(id, stanowisko)
    
);
CREATE TABLE ZAGROZENIA(
    id integer not null,
    stanowisko integer not null,
    wystepowanie varchar(1) not null, -- istnieje / nie istnieje
    czas varchar(1), -- stale / dorazne
    przyczyna varchar(1), -- ludzie / natura
    uzytkownik varchar(1), -- wypelniane jezeli przyczyna == ludzie: uzytkownik spoleczny / prywatny
    uwagi varchar(255),
    CONSTRAINT zagrozenia_pkey PRIMARY KEY (id),
    CONSTRAINT check_wystepowanie CHECK (wystepowanie in ('I','N')),
    CONSTRAINT check_przyczyna CHECK (przyczyna in ('L','N')),
    CONSTRAINT check_uzytkownik CHECK (uzytkownik in ('S','P')),
    CONSTRAINT check_czas CHECK (czas in ('S','D')),
    constraint unique_zagrozenia_st unique(id, stanowisko)
);
CREATE TABLE aktualnosci(
  id integer NOT NULL,
  stanowisko integer NOT NULL,
  magazyn varchar(20),
  nr_inwentarza varchar(20),
  nr_krz varchar(20), -- nr rejestru zabytkow
  data_krz date, -- data wpisu do rejestru
  park character varying(20), -- park kulturowy
  plan character varying(50),
  wlasciciel varchar(500),
  uwagi varchar(255),
  CONSTRAINT aktualnosci_pkey PRIMARY KEY (id)
);
CREATE TABLE fakty
(
    id integer, 
    stanowisko integer, 
    okresa varchar(2),
    okresb varchar(2),
    okr_relacja varchar(1) check (okr_relacja in ('Z','P')),
    okr_pewnosc decimal(3,2),
    jeda varchar(6), 
    jedb varchar(6), 
    jed_relacja varchar(1) check (jed_relacja in ('Z','P')), 
    jed_pewnosc decimal(3,2), 
    funkcja varchar(8), 
    fun_pewnosc decimal(3,2), 
    masowy varchar(50), 
    wydzielony varchar(50),
     CONSTRAINT fakty_pkey PRIMARY KEY (id),
     constraint okresa_okresy_dziejow_fkey foreign key(okresa) references okresy_dziejow(kod),
     constraint okresb_okresy_dziejow_fkey foreign key(okresb) references okresy_dziejow(kod),
     constraint jeda_jednostki_fkey foreign key(jeda) references jednostki(kod),
     constraint jedb_jednostki_fkey foreign key(jedb) references jednostki(kod),
     constraint funkcja_funkcje_fkey foreign key(funkcja) references funkcje(kod)
);
CREATE TABLE funkcje (
    kod varchar(8) primary key, 
    funkcja varchar(20), 
    czlon1 varchar(30), 
    czlon2 varchar(30), 
    czlon3 varchar(30), 
    nazwa varchar(90), 
    skrot varchar(20)
);
CREATE TABLE geometry_columns (
f_table_name TEXT NOT NULL,
f_geometry_column TEXT NOT NULL,
type TEXT NOT NULL,
coord_dimension TEXT NOT NULL,
srid INTEGER NOT NULL,
spatial_index_enabled INTEGER NOT NULL,
CONSTRAINT pk_geom_cols PRIMARY KEY (f_table_name, f_geometry_column),
CONSTRAINT fk_gc_srs FOREIGN KEY (srid) REFERENCES spatial_ref_sys (srid));
CREATE TABLE geometry_columns_auth (
f_table_name VARCHAR(256) NOT NULL,
f_geometry_column VARCHAR(256) NOT NULL,
read_only INTEGER NOT NULL,
hidden INTEGER NOT NULL,
CONSTRAINT pk_gc_auth PRIMARY KEY (f_table_name, f_geometry_column),
CONSTRAINT fk_gc_auth FOREIGN KEY (f_table_name, f_geometry_column) REFERENCES geometry_columns (f_table_name, f_geometry_column) ON DELETE CASCADE);
CREATE TABLE gleba_dane -- gleby 
(
    id integer NOT NULL,
  stanowisko integer NOT NULL,
  luzna character varying(1) check (luzna in ('T','N')),
  zwiezla character varying(1) check (zwiezla in ('T','N')),
  torf_bag character varying(1) check (torf_bag in ('T','N')),
  kamienistosc character varying(1) check (kamienistosc in ('M','S','D')),
  uwagi character varying(255),
    CONSTRAINT gleba_dane_pkey PRIMARY KEY (id),
  constraint gleba_dane_st_fkey foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade,
      constraint unique_gleba_dane_st unique(id, stanowisko)
);
CREATE TABLE gminy (
    id integer primary key, 
    start varchar(2) not null, 
    nazwa varchar(50)
);
CREATE TABLE jednostki (
    kod varchar(6) primary key, 
    okres varchar(1), 
    czlon1 varchar(30), 
    czlon2 varchar(30), 
    nazwa varchar(30), 
    skrot varchar(15), 
    start varchar(2)
);
CREATE TABLE karty -- do kazdego stanowiska mozna dodac informacje o wypelnionej karcie azp
(
  id integer not null,
  stanowisko integer NOT NULL,
  nazwa_lok varchar(50),
  arkusz_mapy varchar(10),
  dalsze_losy varchar(100),
  dzieje_badan varchar(100),
  metryka_hist varchar(10),
  literatura varchar(100),
  dzialka_geodezyjna varchar(255),
  egb character varying(500) ,
  autorzy character varying(255),
  chronologia character varying(255), -- okreslil chronologie
  konsultant character varying(255), -- sprawdzil
  uwagi varchar(255),
  CONSTRAINT pk_karty PRIMARY KEY (id)
);
CREATE TABLE miejsca(
  id integer NOT NULL,
  nazwa varchar(50), 
  rodzaj_badan varchar(2) not null default '?', -- L - lot, P - powierzchniowe, W - weryfikacje,? - nieokreslone
  data varchar(10) not null,
  autor varchar(100) not null,
  uwagi varchar(255),
  wspolrzedne POINT,
  CONSTRAINT pk_miejsca PRIMARY KEY (id)
);
CREATE TABLE miejscowosci (
    id integer primary key, 
    start varchar(2) not null, 
    nazwa varchar(50));
CREATE TABLE okresy_dziejow ( kod varchar(2) not null, kod_epoka varchar(1) not null, epoka varchar(20) not null, okres varchar(30), nazwa varchar(30) not null, skrot varchar(20) not null, constraint okresy_dziejow_pkey primary key (kod));
CREATE TABLE powiaty(
    id integer primary key, 
    start varchar(2) not null, 
    nazwa varchar(50)
);
CREATE TABLE spatial_ref_sys (
srid INTEGER NOT NULL PRIMARY KEY,
auth_name TEXT NOT NULL,
auth_srid INTEGER NOT NULL,
ref_sys_name TEXT,
proj4text TEXT NOT NULL,
srs_wkt TEXT);
CREATE TABLE spatialite_history (
event_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
table_name TEXT NOT NULL,
geometry_column TEXT,
event TEXT NOT NULL,
timestamp TEXT NOT NULL,
ver_sqlite TEXT NOT NULL,
ver_splite TEXT NOT NULL);
CREATE TABLE trasy(
  id integer NOT NULL,
  rodzaj_badan varchar(2) not null default '?', -- L - lot, P - powierzchniowe, W - weryfikacje, ? - nieokreslone
  data varchar(10) not null,
  autor varchar(100) not null,
  rozpoczecie varchar(25),
  zakonczenie varchar(25),
  czestotliwosc integer default 0, -- czestotliwosc odczytow w sekundach
  uwagi varchar(255),
  wspolrzedne LINESTRING,
  CONSTRAINT pk_trasy PRIMARY KEY (id)
);
CREATE TABLE views_geometry_columns (
view_name TEXT NOT NULL,
view_geometry TEXT NOT NULL,
view_rowid TEXT NOT NULL,
f_table_name VARCHAR(256) NOT NULL,
f_geometry_column VARCHAR(256) NOT NULL,
CONSTRAINT pk_geom_cols_views PRIMARY KEY (view_name, view_geometry),
CONSTRAINT fk_views_geom_cols FOREIGN KEY (f_table_name, f_geometry_column) REFERENCES geometry_columns (f_table_name, f_geometry_column) ON DELETE CASCADE);
CREATE TABLE virts_geometry_columns (
virt_name TEXT NOT NULL,
virt_geometry TEXT NOT NULL,
type VARCHAR(30) NOT NULL,
srid INTEGER NOT NULL,
CONSTRAINT pk_geom_cols_virts PRIMARY KEY (virt_name, virt_geometry),
CONSTRAINT fk_vgc_srid FOREIGN KEY (srid) REFERENCES spatial_ref_sys (srid));
CREATE TABLE wojewodztwa (
    id integer primary key, 
    start varchar(2) not null, 
    nazwa varchar(50));
CREATE VIEW geom_cols_ref_sys AS
SELECT f_table_name, f_geometry_column, type,
coord_dimension, spatial_ref_sys.srid AS srid,
auth_name, auth_srid, ref_sys_name, proj4text
FROM geometry_columns, spatial_ref_sys
WHERE geometry_columns.srid = spatial_ref_sys.srid;
CREATE UNIQUE INDEX idx_spatial_ref_sys 
ON spatial_ref_sys (auth_srid, auth_name);
CREATE INDEX idx_srid_geocols ON geometry_columns
(srid);
CREATE INDEX idx_viewsjoin ON views_geometry_columns
(f_table_name, f_geometry_column);
CREATE INDEX idx_virtssrid ON virts_geometry_columns
(srid);
CREATE TRIGGER del_stanowisko before delete on stanowiska 
begin
    delete from ekspozycja_dane where stanowisko = OLD.id;
    delete from fizgeo_dane where stanowisko = OLD.id;
    delete from teren_dane where stanowisko = OLD.id;
    delete from wnioski where stanowisko = OLD.id;
    delete from zagrozenia where stanowisko = OLD.id;
    delete from fakty where stanowisko = OLD.id;
    delete from karty where stanowisko = OLD.id;
    delete from obszar_dane where stanowisko = OLD.id;
    delete from aktualnosci where stanowisko = OLD.id;
    delete from media where id = (select medium from st_media where stanowisko = OLD.id);
    delete from st_media where stanowisko = OLD.id;
end;
CREATE TRIGGER "ggi_miejsca_wspolrzedne" BEFORE INSERT ON miejsca
FOR EACH ROW BEGIN
SELECT RAISE(ROLLBACK, 'miejsca.wspolrzedne violates Geometry constraint [geom-type or SRID not allowed]')
WHERE (SELECT type FROM geometry_columns
WHERE f_table_name = 'miejsca' AND f_geometry_column = 'wspolrzedne'
AND GeometryConstraints(NEW.wspolrzedne, type, srid, 'XY') = 1) IS NULL;
END;
CREATE TRIGGER "ggi_stanowiska_wspolrzedne" BEFORE INSERT ON stanowiska
FOR EACH ROW BEGIN
SELECT RAISE(ROLLBACK, 'stanowiska.wspolrzedne violates Geometry constraint [geom-type or SRID not allowed]')
WHERE (SELECT type FROM geometry_columns
WHERE f_table_name = 'stanowiska' AND f_geometry_column = 'wspolrzedne'
AND GeometryConstraints(NEW.wspolrzedne, type, srid, 'XY') = 1) IS NULL;
END;
CREATE TRIGGER "ggi_trasy_wspolrzedne" BEFORE INSERT ON trasy
FOR EACH ROW BEGIN
SELECT RAISE(ROLLBACK, 'trasy.wspolrzedne violates Geometry constraint [geom-type or SRID not allowed]')
WHERE (SELECT type FROM geometry_columns
WHERE f_table_name = 'trasy' AND f_geometry_column = 'wspolrzedne'
AND GeometryConstraints(NEW.wspolrzedne, type, srid, 'XY') = 1) IS NULL;
END;
CREATE TRIGGER "ggu_miejsca_wspolrzedne" BEFORE UPDATE ON miejsca
FOR EACH ROW BEGIN
SELECT RAISE(ROLLBACK, 'miejsca.wspolrzedne violates Geometry constraint [geom-type or SRID not allowed]')
WHERE (SELECT type FROM geometry_columns
WHERE f_table_name = 'miejsca' AND f_geometry_column = 'wspolrzedne'
AND GeometryConstraints(NEW.wspolrzedne, type, srid, 'XY') = 1) IS NULL;
END;
CREATE TRIGGER "ggu_stanowiska_wspolrzedne" BEFORE UPDATE ON stanowiska
FOR EACH ROW BEGIN
SELECT RAISE(ROLLBACK, 'stanowiska.wspolrzedne violates Geometry constraint [geom-type or SRID not allowed]')
WHERE (SELECT type FROM geometry_columns
WHERE f_table_name = 'stanowiska' AND f_geometry_column = 'wspolrzedne'
AND GeometryConstraints(NEW.wspolrzedne, type, srid, 'XY') = 1) IS NULL;
END;
CREATE TRIGGER "ggu_trasy_wspolrzedne" BEFORE UPDATE ON trasy
FOR EACH ROW BEGIN
SELECT RAISE(ROLLBACK, 'trasy.wspolrzedne violates Geometry constraint [geom-type or SRID not allowed]')
WHERE (SELECT type FROM geometry_columns
WHERE f_table_name = 'trasy' AND f_geometry_column = 'wspolrzedne'
AND GeometryConstraints(NEW.wspolrzedne, type, srid, 'XY') = 1) IS NULL;
END;
CREATE TABLE st_media(medium integer, stanowisko integer, typ varchar(1));
CREATE TABLE media(id integer not null primary key, sygnatura varchar(50), plik varchar(20), format varchar(4), tabela varchar(1), dane blob);
CREATE TABLE ustawienia(klucz varchar(10) primary key, wartosc varchar(20));
INSERT INTO "geometry_columns" VALUES('trasy','wspolrzedne','LINESTRING','XY',2180,0);
INSERT INTO "geometry_columns" VALUES('miejsca','wspolrzedne','POINT','XY',2180,0);
INSERT INTO "geometry_columns" VALUES('stanowiska','wspolrzedne','POLYGON','XY',2180,0);
insert into ustawienia values('wersja','0001');
