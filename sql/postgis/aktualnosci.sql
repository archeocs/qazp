CREATE TABLE aktualnosci -- aktualna ochrona
(
  id integer NOT NULL,
  stanowisko integer NOT NULL,
  magazyn varchar(20),
  nr_inwentarza varchar(20),
  nr_krz varchar(20), -- nr rejestru zabytkow
  data_krz date, -- data wpisu do rejestru
  park character varying(20), -- park kulturowy
  plan character varying(50),
  wlasciciel varchar(500),
  uwagi varchar(255)
  CONSTRAINT aktualnosci_pkey PRIMARY KEY (id),
);
