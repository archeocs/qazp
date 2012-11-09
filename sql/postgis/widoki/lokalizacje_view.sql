-- View: lokalizacje_view

-- DROP VIEW lokalizacje_view;

CREATE OR REPLACE VIEW lokalizacje_view AS 
 SELECT l.id, l.obszar, l.nr_obszar, m.nazwa AS miejscowosc, l.nr_miejscowosc, g.nazwa AS gmina, p.nazwa AS powiat, w.nazwa AS wojewodztwo, m.id AS miej_id, g.id AS gmina_id, p.id AS powiat_id, w.id AS woj_id
   FROM lokalizacje l
   JOIN miejscowosci m ON l.miejscowosc = m.id
   JOIN gminy g ON l.gmina = g.id
   LEFT JOIN powiaty p ON l.powiat = p.id
   LEFT JOIN wojewodztwa w ON l.wojewodztwo = w.id;

ALTER TABLE lokalizacje_view OWNER TO milosz;

