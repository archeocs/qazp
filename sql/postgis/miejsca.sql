drop table miejsca;
CREATE TABLE miejsca(
  id integer NOT NULL,
  nazwa varchar(50), 
  rodzaj_badan varchar(1) not null default '?', -- L - lot, P - powierzchniowe, W - weryfikacje,? - nieokreslone
  data date,
  autor varchar(100) ,
  uwagi varchar(255),
  wspolrzedne geometry,
  CONSTRAINT miejsca_pkey PRIMARY KEY (id),
  CONSTRAINT enforce_dims_wspolrzedne_miejsca CHECK (st_ndims(wspolrzedne) = 2),
  CONSTRAINT enforce_geotype_wspolrzedne_miejsca CHECK (geometrytype(wspolrzedne) = 'POINT'::text OR wspolrzedne IS NULL),
  CONSTRAINT enforce_srid_wspolrzedne_miejsca CHECK (st_srid(wspolrzedne) = 2180),
  CONSTRAINT miejsca_check_rodzaj CHECK (rodzaj_badan::text = ANY (ARRAY['?'::character varying, 'W'::character varying, 'P'::character varying, 'A'::character varying, 'X'::character varying, 'L'::character varying]::text[]))
)
WITH (
  OIDS=FALSE
);
ALTER TABLE trasy OWNER TO milosz;
delete from geometry_columns where f_table_name='miejsca';
insert into geometry_columns values('','public','miejsca','wspolrzedne',2,2180,'POINT');
