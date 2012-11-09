-- Table: lokalizacje

DROP TABLE lokalizacje;

CREATE TABLE lokalizacje
(
  id integer NOT NULL,
  obszar character varying(8) NOT NULL,
  nr_obszar character varying(8),
  miejscowosc integer NOT NULL,
  nr_miejscowosc varchar(8) NOT NULL,
  gmina integer NOT NULL,
  powiat integer,
  wojewodztwo integer,
  CONSTRAINT lokalizacje_pkey PRIMARY KEY (id),
  CONSTRAINT fk_nazwa_gmina FOREIGN KEY (gmina)
      REFERENCES gminy (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_nazwa_miejscowosc FOREIGN KEY (miejscowosc)
      REFERENCES miejscowosci (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_nazwa_powiat FOREIGN KEY (powiat)
      REFERENCES powiaty (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_nazwa_wojewodztwo FOREIGN KEY (wojewodztwo)
      REFERENCES wojewodztwa (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT uq_lokalizacje_miejscowosc UNIQUE (miejscowosc, nr_miejscowosc),
  CONSTRAINT uq_lokalizacje_obszar UNIQUE (obszar, nr_obszar)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE lokalizacje OWNER TO milosz;

-- Trigger: nowy_id_lokalizacja on lokalizacje

-- DROP TRIGGER nowy_id_lokalizacja ON lokalizacje;

CREATE TRIGGER nowy_id_lokalizacja
  BEFORE INSERT
  ON lokalizacje
  FOR EACH ROW
  EXECUTE PROCEDURE fun_new_id();

