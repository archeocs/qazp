drop table trasy;
CREATE TABLE trasy(
  id integer NOT NULL,
  rozpoczecie timestamp,
  zakonczenie timestamp,
  czestotliwosc integer default 0, -- czestotliwosc odczytow w sekundach
  rodzaj_badan varchar(1) not null default '?', -- L - lot, P - powierzchniowe, W - weryfikacje, ? - nieokreslone
  data date,
  autor varchar(100),
  uwagi varchar(255),
  wspolrzedne geometry,
  CONSTRAINT trasy_pkey PRIMARY KEY (id),
  CONSTRAINT enforce_dims_wspolrzedne_trasy CHECK (st_ndims(wspolrzedne) = 2),
  CONSTRAINT enforce_geotype_wspolrzedne_trasy CHECK (geometrytype(wspolrzedne) = 'LINESTRING'::text OR wspolrzedne IS NULL),
  CONSTRAINT enforce_srid_wspolrzedne_trasy CHECK (st_srid(wspolrzedne) = 2180),
  CONSTRAINT trasy_check_rodzaj CHECK (rodzaj_badan::text = ANY (ARRAY['?'::character varying, 'W'::character varying, 'P'::character varying, 'A'::character varying, 'X'::character varying, 'L'::character varying]::text[]))
)
WITH (
  OIDS=FALSE
);
ALTER TABLE trasy OWNER TO milosz;
delete from geometry_columns where f_table_name='trasy';
insert into geometry_columns values('','public','trasy','wspolrzedne',2,2180,'LINESTRING');
