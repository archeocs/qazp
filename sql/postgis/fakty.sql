CREATE TABLE fakty
(
    id integer, 
    stanowisko integer, 
    okres varchar(1), 
    jed1 varchar(10), 
    jed2 varchar(10), 
    relacja varchar(10) check (relacja in ('L','O')), 
    pewnosc decimal(3,2), 
    funkcja varchar(1), 
    rodzaj_fun varchar(10), 
    masowy varchar(20), 
    wydzielony varchar(20)
     CONSTRAINT fakty_pkey PRIMARY KEY (id),
  constraint fakty_st_fkey foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade,
)
WITH (
  OIDS=FALSE
);
ALTER TABLE fakty OWNER TO milosz;
