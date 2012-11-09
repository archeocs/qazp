-- drop table aktualnosci;
CREATE TABLE informacje -- informacje dotyczace lokalizacji
(
  id integer NOT NULL,
  obiekt integer not null, -- obiekt do ktorego odnosi sie informacja (miejsce, trasa, lokalizacja, inne)
  klucz varchar(20) NOT null, -- mozna przypisac klucz, np w celu latwiejszego przeszukiwania. Kilka zastrzezonych: LITERATURA, DOKUMENTACJA, ...
  wartosc character varying(255) not null, -- park kulturowy
  data date not null, -- data wprowadzenia informacji
  CONSTRAINT pk_informacje PRIMARY KEY (id)
);