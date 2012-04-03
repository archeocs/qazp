-- CREATE VIRTUAL TABLE SpatialIndex USING VirtualSpatialIndex();
CREATE TABLE ekspozycje
(
  eid integer NOT NULL,
  stanowisko integer NOT NULL,
  eksponowany varchar(1) NOT NULL DEFAULT 'N',
  kraw_stok varchar(1) NOT NULL DEFAULT 'N',
  sfal_cypel varchar(1) NOT NULL DEFAULT 'N',
  cypl varchar(1) NOT NULL DEFAULT 'N',
  wal_garb varchar(1) NOT NULL DEFAULT 'N',
  okrezna varchar(1) NOT NULL DEFAULT 'N',
  osloniety varchar(1) NOT NULL DEFAULT 'N',
  podst_stoku varchar(1) NOT NULL DEFAULT 'N',
  dolina_niecka varchar(1) NOT NULL DEFAULT 'N',
  kotl_zagl varchar(1) NOT NULL DEFAULT 'N',
  jaskinia varchar(1) NOT NULL DEFAULT 'N',
  forma_szczegolna varchar(255) NOT NULL DEFAULT 'N',
  kier_n varchar(1) NOT NULL DEFAULT 'N',
  kier_ne varchar(1) NOT NULL DEFAULT 'N',
  kier_e varchar(1) NOT NULL DEFAULT 'N',
  kier_se varchar(1) NOT NULL DEFAULT 'N',
  kier_s varchar(1) NOT NULL DEFAULT 'N',
  kier_sw varchar(1) NOT NULL DEFAULT 'N',
  kier_w varchar(1) NOT NULL DEFAULT 'N',
  kier_nw varchar(1) NOT NULL DEFAULT 'N',
  CONSTRAINT pk_eid PRIMARY KEY (eid)
);
CREATE TABLE epoki_slo
(
  sid integer NOT NULL,
  nazwa varchar(30),
  CONSTRAINT pk_epoki PRIMARY KEY (sid)
);
CREATE TABLE funkcje_slo
(
  sid integer NOT NULL,
  nazwa varchar(30),
  CONSTRAINT pk_funkcje PRIMARY KEY (sid)
);

CREATE TABLE gminy_slo
(
  sid integer NOT NULL,
  nazwa varchar(30),
  CONSTRAINT pk_gmina PRIMARY KEY (sid)
);
CREATE TABLE kultury_slo
(
  sid integer NOT NULL,
  nazwa varchar(30),
  CONSTRAINT pk_kultury PRIMARY KEY (sid)
);
CREATE TABLE lokalizacje
(
  lid integer NOT NULL,
  arkusz varchar(8) NOT NULL,
  nr_arkusz varchar(8) NOT NULL,
  miejscowosc integer NOT NULL,
  nr_miejscowosc varchar(8) NOT NULL,
  gmina integer NOT NULL,
  powiat integer,
  wojewodztwo integer,
  CONSTRAINT pk_lokalizacja PRIMARY KEY (lid)
);
CREATE TABLE materialy
(
  mid integer NOT NULL,
  stanowisko integer NOT NULL,
  epoka integer DEFAULT 0,
  kultura integer DEFAULT 0,
  funkcja integer DEFAULT 0,
  ceramika integer DEFAULT 0,
  kamien integer DEFAULT 0,
  metal integer DEFAULT 0,
  masowy varchar(255) DEFAULT NULL,
  wyodrebniony varchar(255) DEFAULT NULL,
  CONSTRAINT pk_mat PRIMARY KEY (mid)
);
CREATE TABLE miasta_slo
(
  sid integer NOT NULL,
  nazwa varchar(30),
  CONSTRAINT pk_miejsc PRIMARY KEY (sid)
);
CREATE TABLE obszary
(
  oid integer NOT NULL,
  stanowisko integer NOT NULL,
  obserwacja integer,
  pole integer,
  nasycenie integer,
  gestosc integer,
  powierzchnia integer,
  centrycznosc integer,
  CONSTRAINT pk_oid PRIMARY KEY (oid)
);
CREATE TABLE polozenia
(
  pid integer NOT NULL,
  stanowisko integer NOT NULL,
  nadmorska varchar(1) NOT NULL DEFAULT 'N',
  morze varchar(1) NOT NULL DEFAULT 'N',
  plaza varchar(1) NOT NULL DEFAULT 'N',
  mierzeja varchar(1) NOT NULL DEFAULT 'N',
  skarpa varchar(1) NOT NULL DEFAULT 'N',
  wal_wydma varchar(1) NOT NULL DEFAULT 'N',
  duza_dol varchar(1) NOT NULL DEFAULT 'N',
  woda varchar(1) NOT NULL DEFAULT 'N',
  terasa_denna varchar(1) NOT NULL DEFAULT 'N',
  terasa_nadzalew varchar(1) NOT NULL DEFAULT 'N',
  terasa_wyzsza varchar(1) NOT NULL DEFAULT 'N',
  brzeg_wys varchar(1) NOT NULL DEFAULT 'N',
  mala_dol varchar(1) NOT NULL DEFAULT 'N',
  dno_doliny varchar(1) NOT NULL DEFAULT 'N',
  stok_doliny varchar(1) NOT NULL DEFAULT 'N',
  kraw_doliny varchar(1) NOT NULL DEFAULT 'N',
  poza_dol varchar(1) NOT NULL DEFAULT 'N',
  rownina varchar(1) NOT NULL DEFAULT 'N',
  obsz_falisty varchar(1) NOT NULL DEFAULT 'N',
  obsz_pagor varchar(1) NOT NULL DEFAULT 'N',
  obszar_gorz varchar(1) NOT NULL DEFAULT 'N',
  CONSTRAINT pk_pid PRIMARY KEY (pid)
);
CREATE TABLE powiaty_slo
(
  sid integer NOT NULL,
  nazwa varchar(30),
  CONSTRAINT pk_powiat PRIMARY KEY (sid)
);

CREATE TABLE trasy(
  id integer NOT NULL,
  rodzaj_badan varchar(2) not null, -- L - lot, P - powierzchniowe, W - weryfikacje
  data varchar(10) not null,
  autor varchar(100) not null,
  rozpoczecie varchar(25) not null,
  zakonczenie varchar(25) not null,
  czestotliwosc integer not null, -- czestotliwosc odczytow w sekundach
  uwagi varchar(255),
  wspolrzedne LINESTRING,
  CONSTRAINT pk_trasy PRIMARY KEY (id)
);

CREATE TABLE stanowiska
(
  sid integer NOT NULL,
  rodzaj varchar(7) NOT NULL,
  arkusz varchar(8) NOT NULL,
  nr_arkusz varchar(8) NOT NULL,
  miejscowosc varchar(30) NOT NULL,
  nr_miejscowosc varchar(8) NOT NULL,
  -- wspolrzedne geometry,
  autor varchar(40),
  data varchar(10),
  lokalizacja integer, 
  wspolrzedne POLYGON,
  CONSTRAINT stanowiska_pkey PRIMARY KEY (sid)
--  CONSTRAINT enforce_dims_wspolrzedne CHECK (st_ndims(wspolrzedne) = 2),
--  CONSTRAINT enforce_geotype_wspolrzedne CHECK (geometrytype(wspolrzedne) = 'POLYGON'::text OR wspolrzedne IS NULL),
--  CONSTRAINT enforce_srid_wspolrzedne CHECK (st_srid(wspolrzedne) = 3452)
);

CREATE TABLE tereny
(
  tid integer NOT NULL,
  stanowisko integer NOT NULL,
  pole_orne varchar(1) NOT NULL DEFAULT 'N',
  sad varchar(1) NOT NULL DEFAULT 'N',
  prywatny varchar(1) NOT NULL DEFAULT 'N',
  spoleczny varchar(1) NOT NULL DEFAULT 'N',
  park varchar(1) NOT NULL DEFAULT 'N',
  laka varchar(1) NOT NULL DEFAULT 'N',
  przemyslowy varchar(1) NOT NULL DEFAULT 'N',
  las varchar(1) NOT NULL DEFAULT 'N',
  zabud varchar(1) NOT NULL DEFAULT 'N',
  niezabud varchar(1) NOT NULL DEFAULT 'N',
  srednio_zabud varchar(1) NOT NULL DEFAULT 'N',
  okresl_blizsze varchar(255) DEFAULT NULL,
  CONSTRAINT pk_tid PRIMARY KEY (tid)
);

CREATE TABLE wnioski
(
  wid integer NOT NULL,
  stanowisko integer NOT NULL,
  wart_pozn integer,
  inwentaryzacja varchar(1) NOT NULL DEFAULT 'N',
  interwencja varchar(1) NOT NULL DEFAULT 'N',
  wykopaliska varchar(1) NOT NULL DEFAULT 'N',
  dodatkowe varchar(255) DEFAULT NULL,
  CONSTRAINT pk_wid PRIMARY KEY (wid)
);
CREATE TABLE wojewodztwa_slo
(
  sid integer NOT NULL,
  nazwa varchar(30),
  CONSTRAINT pk_woj PRIMARY KEY (sid)
);
CREATE TABLE zagrozenia
(
  zid integer NOT NULL,
  stanowisko integer NOT NULL,
  istnieje varchar(1) NOT NULL DEFAULT 'N',
  stale varchar(1) NOT NULL DEFAULT 'N',
  ludzie varchar(1) NOT NULL DEFAULT 'N',
  natura varchar(1) NOT NULL DEFAULT 'N',
  prywatny varchar(1) NOT NULL DEFAULT 'N',
  spoleczny varchar(1) NOT NULL DEFAULT 'N',
  dodatkowe varchar(255) DEFAULT NULL,
  CONSTRAINT pk_zid PRIMARY KEY (zid)
);

INSERT INTO geometry_columns VALUES('stanowiska','wspolrzedne','POLYGON','XY',2180,0);
INSERT INTO geometry_columns VALUES('trasy','wspolrzedne','LINESTRING','XY',2180,0);

CREATE TRIGGER "ggi_stanowiska_wspolrzedne" BEFORE INSERT ON stanowiska
FOR EACH ROW BEGIN
SELECT RAISE(ROLLBACK, 'stanowiska.wspolrzedne violates Geometry constraint [geom-type or SRID not allowed]')
WHERE (SELECT type FROM geometry_columns
WHERE f_table_name = 'stanowiska' AND f_geometry_column = 'wspolrzedne'
AND GeometryConstraints(NEW.wspolrzedne, type, srid, 'XY') = 1) IS NULL;
END;
CREATE TRIGGER "ggu_stanowiska_wspolrzedne" BEFORE UPDATE ON stanowiska
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
CREATE TRIGGER "ggu_trasy_wspolrzedne" BEFORE UPDATE ON trasy
FOR EACH ROW BEGIN
SELECT RAISE(ROLLBACK, 'trasy.wspolrzedne violates Geometry constraint [geom-type or SRID not allowed]')
WHERE (SELECT type FROM geometry_columns
WHERE f_table_name = 'trasy' AND f_geometry_column = 'wspolrzedne'
AND GeometryConstraints(NEW.wspolrzedne, type, srid, 'XY') = 1) IS NULL;
END;

