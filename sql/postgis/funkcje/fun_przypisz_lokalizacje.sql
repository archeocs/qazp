CREATE FUNCTION fun_przypisz_lokalizacje() RETURNS trigger AS
$fun_przypisz_lokalizacje$
declare
 id_lok integer default null;
begin
select id from lokalizacje where obszar = NEW.obszar and nr_obszar = NEW.obszr into id_lok;
 if id_lok is not null then
     NEW.lokalizacja  := id_lok;
 end if;
 return NEW;
 end;
 $fun_przypisz_lokalizacje$
LANGUAGE plpgsql VOLATILE;
ALTER FUNCTION fun_przypisz_lokalizacje() OWNER TO milosz;
