CREATE TABLE epoki
(
  id integer NOT NULL,
  nazwa character varying(30) not null,
  constraint pk_epoki primary key(id),
  constraint uq_epoki_nazwa unique(nazwa)
  
)
WITH (
  OIDS=FALSE
);
ALTER TABLE miejsca OWNER TO milosz;
