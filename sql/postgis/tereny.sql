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
    rolniczy varchar(1) check (rolniczy in ('T','N')),
    spoleczny varchar(1) check (spoleczny in ('T','N')),
    przemyslowy varchar(1) check (przemyslowy in ('T','N')),
    utwor_geo varchar(1) check (utwor_geo in ('L','Z','T')), -- utwor geologiczny L - luzny, Z - zwiezly, T-torf-bag
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
