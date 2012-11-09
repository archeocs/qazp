-- View: stanowiska_view

-- DROP VIEW stanowiska_view;

CREATE OR REPLACE VIEW stanowiska_view AS 
 SELECT COALESCE(v.obszar, s.obszar) AS obszar, COALESCE(v.nr_obszar, s.nr_obszar) AS nr_obszar, COALESCE(v.miejscowosc, s.miejscowosc) AS miejscowosc, COALESCE(v.nr_miejscowosc, s.nr_miejscowosc) AS nr_miejscowosc, v.gmina, v.powiat, v.wojewodztwo, s.autor, s.data, s.rodzaj, s.id as stanowisko, v.id as lokalizacja
   FROM stanowiska s
   LEFT JOIN lokalizacje_view v ON s.lokalizacja = v.id;

ALTER TABLE stanowiska_view OWNER TO milosz;

