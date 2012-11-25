--drop table gleby
CREATE TABLE gleba_dane -- gleby 
(
  id integer NOT NULL,
  stanowisko integer NOT NULL,
  luzna character varying(1) check (luzna in ('T','N')),
  zwiezla character varying(1) check (zwiezla in ('T','N')),
  torf_bag character varying(1) check (torf_bag in ('T','N')),
  kamienistosc character varying(1) check (kamienistosc in ('M','S','D')),
  uwagi character varying(255),
    CONSTRAINT gleba_dane_pkey PRIMARY KEY (id),
  constraint gleba_dane_st_fkey foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade,
      constraint unique_gleba_dane_st unique(id, stanowisko)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE gleba_dane OWNER TO milosz;
