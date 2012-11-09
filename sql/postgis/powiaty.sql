CREATE TABLE powiaty
(
  id integer NOT NULL,
  nazwa character varying(30) not null,
  constraint pk_powiaty primary key(id),
  constraint uq_powiaty_nazwa unique(nazwa)
  
)
WITH (
  OIDS=FALSE
);
ALTER TABLE miejsca OWNER TO milosz;
