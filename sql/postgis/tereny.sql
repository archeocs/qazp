drop table teren_dane;
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
    prywatny varchar(1) check (rolniczy in ('T','N')),
    spoleczny varchar(1) check (spoleczny in ('T','N')),
    przemyslowy varchar(1) check (przemyslowy in ('T','N')),
    uwagi varchar(255), 
    CONSTRAINT teren_dane_pkey PRIMARY KEY (id),
  constraint teren_dane_st_fkey foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade,
      constraint unique_teren_dane_st unique(id, stanowisko)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE teren_dane OWNER TO milosz;
