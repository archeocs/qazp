drop table karty;
create table karty (
id integer NOT NULL,
  stanowisko integer NOT NULL,
  nazwa_lok varchar(50),
  arkusz_mapy varchar(10),
  dalsze_losy varchar(100),
  dzieje_badan varchar(100),
  metryka_hist varchar(10),
  literatura varchar(100),
  dzialka_geodezyjna varchar(255),
  egb character varying(500) ,
  autorzy character varying(255),
  chronologia character varying(255), -- okreslil chronologie
  konsultant character varying(255), -- sprawdzil
  uwagi varchar(255),
  CONSTRAINT karty_pkey PRIMARY KEY (id)
)
