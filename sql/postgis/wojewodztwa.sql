CREATE TABLE wojewodztwa
(
  id integer NOT NULL,
  nazwa character varying(30) not null,
  constraint pk_wojewodztwa primary key(id),
  constraint uq_wojewodztwa_nazwa unique(nazwa)
  
)
WITH (
  OIDS=FALSE
);
ALTER TABLE miejsca OWNER TO milosz;
