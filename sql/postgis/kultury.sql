CREATE TABLE kultury
(
  id integer NOT NULL,
  nazwa character varying(30) not null,
  constraint pk_kultury primary key(id),
  constraint uq_kultury_nazwa unique(nazwa)
  
)
WITH (
  OIDS=FALSE
);
ALTER TABLE miejsca OWNER TO milosz;
