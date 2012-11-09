-- Table: polozenia

DROP TABLE fizgeo_dane;

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
    CONSTRAINT fizgeo_dane_st_fkey FOREIGN KEY (stanowisko)
      REFERENCES stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
    constraint unique_fizgeo_dane_st unique(id, stanowisko)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE fizgeo_dane OWNER TO milosz;
