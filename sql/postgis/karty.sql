drop table karty;
CREATE TABLE karty -- do kazdego stanowiska mozna dodac informacje o wypelnionej karcie azp
(
  id integer NOT NULL,
  stanowisko integer NOT NULL,
  szerokosc decimal(9,6) null, -- szerokosc geograficzna
  dlugosc decimal(9,6) null, -- dlugosc geograficzna
  nr_dzialki character varying(20) null,
  egb character varying(20) null,
  wlasciciel character varying(50) null,
  autorzy character varying(255) null,
  chronologia character varying(255) null,
  konsultant character varying(255) null,
  zbiory character varying(100) null, -- miejsce przechowywania
  nr_inwentarza character varying(20),
  
  CONSTRAINT pk_karty PRIMARY KEY (id),
  constraint fk_stanowisko_karty foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade
  -- rozwazyc ograniczenia check
);