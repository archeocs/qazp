drop table obszary;
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
    constraint obszar_dane_st_fkey foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade,
    CONSTRAINT check_obserwacja CHECK (obserwacja in ('U','B')),
    CONSTRAINT check_pole CHECK (pole in ('O','Z')),
    CONSTRAINT check_nasyc_rozklad CHECK (nasyc_rozklad in ('R','N')),
    CONSTRAINT check_nasyc_typ CHECK (nasyc_typ in ('J','W','D')),
    CONSTRAINT check_gestosc_znal CHECK (gestosc_znal in ('M','S','D')),
    constraint unique_obszar_dane_st unique(id, stanowisko)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE obszar_dane OWNER TO milosz;
