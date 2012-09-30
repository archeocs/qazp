CREATE TABLE trasy(
  id integer NOT NULL,
  rodzaj_badan varchar(2) not null default '?', -- L - lot, P - powierzchniowe, W - weryfikacje, ? - nieokreslone
  data varchar(10) not null,
  autor varchar(100) not null,
  rozpoczecie varchar(25),
  zakonczenie varchar(25),
  czestotliwosc integer default 0, -- czestotliwosc odczytow w sekundach
  uwagi varchar(255),
  wspolrzedne LINESTRING,
  CONSTRAINT pk_trasy PRIMARY KEY (id)
);

INSERT INTO geometry_columns VALUES('trasy','wspolrzedne','LINESTRING','XY',2180,0);

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

CREATE TABLE miejsca(
  id integer NOT NULL,
  nazwa varchar(50), 
  rodzaj_badan varchar(2) not null default '?', -- L - lot, P - powierzchniowe, W - weryfikacje,? - nieokreslone
  data varchar(10) not null,
  autor varchar(100) not null,
  uwagi varchar(255),
  wspolrzedne POINT,
  CONSTRAINT pk_miejsca PRIMARY KEY (id)
);


INSERT INTO geometry_columns VALUES('miejsca','wspolrzedne','POINT','XY',2180,0);

CREATE TRIGGER "ggi_miejsca_wspolrzedne" BEFORE INSERT ON miejsca
FOR EACH ROW BEGIN
SELECT RAISE(ROLLBACK, 'miejsca.wspolrzedne violates Geometry constraint [geom-type or SRID not allowed]')
WHERE (SELECT type FROM geometry_columns
WHERE f_table_name = 'miejsca' AND f_geometry_column = 'wspolrzedne'
AND GeometryConstraints(NEW.wspolrzedne, type, srid, 'XY') = 1) IS NULL;
END;
CREATE TRIGGER "ggu_miejsca_wspolrzedne" BEFORE UPDATE ON miejsca
FOR EACH ROW BEGIN
SELECT RAISE(ROLLBACK, 'miejsca.wspolrzedne violates Geometry constraint [geom-type or SRID not allowed]')
WHERE (SELECT type FROM geometry_columns
WHERE f_table_name = 'miejsca' AND f_geometry_column = 'wspolrzedne'
AND GeometryConstraints(NEW.wspolrzedne, type, srid, 'XY') = 1) IS NULL;
END;

