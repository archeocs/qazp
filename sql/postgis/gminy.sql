CREATE TABLE gminy
(
  id integer NOT NULL,
  nazwa character varying(30) not null,
  constraint pk_gminy primary key(id),
  constraint uq_gminy_nazwa unique(nazwa)
  
)
WITH (
  OIDS=FALSE
);
ALTER TABLE miejsca OWNER TO milosz;
