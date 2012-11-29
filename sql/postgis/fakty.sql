CREATE TABLE fakty
(
    id integer, 
    stanowisko integer, 
    okres1 varchar(10),
    okres2 varchar(10),
    okr_relacja varchar(1) check (okr_relacja in ('Z','P')),
    okr_pewnosc decimal(3,2),
    jed1 varchar(10), 
    jed2 varchar(10), 
    jed_relacja varchar(1) check (jed_relacja in ('Z','P')), 
    jed_pewnosc decimal(3,2), 
    funkcja varchar(1), 
    rodzaj_fun varchar(10),
    fun_pewnosc decimal(3,2), 
    masowy varchar(50), 
    wydzielony varchar(50),
     CONSTRAINT fakty_pkey PRIMARY KEY (id),
  constraint fakty_st_fkey foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade
)
WITH (
  OIDS=FALSE
);
ALTER TABLE fakty OWNER TO milosz;
