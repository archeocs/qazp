-- Table: stanowiska

DROP TABLE stanowiska;

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
    data date,
    autor varchar(100),
    uwagi varchar(255),
    wspolrzedne geometry,
  CONSTRAINT stanowiska_pkey PRIMARY KEY (id),
  CONSTRAINT enforce_dims_wspolrzedne_stanowiska CHECK (st_ndims(wspolrzedne) = 2),
  CONSTRAINT enforce_geotype_wspolrzedne_stanowiska CHECK (geometrytype(wspolrzedne) = 'POLYGON'::text OR wspolrzedne IS NULL),
  CONSTRAINT enforce_srid_wspolrzedne_stanowiska CHECK (st_srid(wspolrzedne) = 2180),
  CONSTRAINT stanowiska_check_rodzaj CHECK (rodzaj_badan::text = ANY (ARRAY['?'::character varying, 'W'::character varying, 'P'::character varying, 'A'::character varying, 'X'::character varying, 'L'::character varying]::text[]))
)
WITH (
  OIDS=FALSE
);
ALTER TABLE stanowiska OWNER TO milosz;
delete from geometry_columns where f_table_name='stanowiska';
insert into geometry_columns values('','public','stanowiska','wspolrzedne',2,2180,'POLYGON');
