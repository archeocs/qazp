drop table ekspozycja_dane;
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
    constraint ekspozycja_dane_pkey primary key(id),
    constraint ekspozycja_dane_st_fkey foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade,
      constraint unique_ekspozycja_dane_st unique(id, stanowisko)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE ekspozycja_dane OWNER TO milosz;
