drop table wnioski;
CREATE TABLE WNIOSKI(
    id integer not null,
    stanowisko integer not null,
    wartosc varchar(1), -- mala / srednia / duza
    inwentaryzacja varchar(1) check (inwentaryzacja in ('T','N')),
    wykopaliska varchar(1) check (wykopaliska in ('T','N')),
    interwencja varchar(1) check (interwencja in ('T','N')),
    uwagi varchar(255),
    CONSTRAINT wnioski_pkey PRIMARY KEY (id),
    constraint wnioski_st_pkey foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade,
    CONSTRAINT check_wartosc CHECK (wartosc in ('M','S','D')),
    constraint unique_wnioski_st unique(id, stanowisko)
    
)
WITH (
  OIDS=FALSE
);
ALTER TABLE wnioski OWNER TO milosz;
