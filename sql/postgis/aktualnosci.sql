-- drop table aktualnosci;
CREATE TABLE aktualnosci -- aktualna ochrona
(
  id integer NOT NULL,
  lokalizacja integer NOT NULL,
  rejestr varchar(20), -- nr rejestru zabytkow
  data date null, -- data wpisu do rejestru
  park character varying(20) null, -- park kulturowy
  plan character varying(50) null,
  CONSTRAINT pk_aktualnosci PRIMARY KEY (id),
  constraint fk_stanowisko_aktualnosci foreign key (lokalizacja) references lokalizacje (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade
);