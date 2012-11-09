-- Function: fun_new_id()

-- DROP FUNCTION fun_new_id();

CREATE OR REPLACE FUNCTION fun_new_id()
  RETURNS trigger AS
$BODY$declare
 mid integer default 0;
begin
 IF TG_TABLE_NAME = 'miejscowosci' then
    select coalesce(max(id),0) from miejscowosci into mid;
 elsif TG_TABLE_NAME = 'gminy' then
    select coalesce(max(id),0) from gminy into mid;
 elsif TG_TABLE_NAME = 'powiaty' then
    select coalesce(max(id),0) from powiaty into mid;
 elsif TG_TABLE_NAME = 'wojewodztwa' then
    select coalesce(max(id),0) from wojewodztwa into mid;
 elsif TG_TABLE_NAME = 'kultury' then
    select coalesce(max(id),0) from kultury into mid;
 elsif TG_TABLE_NAME = 'epoki' then
    select coalesce(max(id),0) from epoki into mid;
 elsif TG_TABLE_NAME = 'funkcje' then
    select coalesce(max(id),0) from funkcje into mid;
 elsif TG_TABLE_NAME = 'aktualnosci' then
    select coalesce(max(id),0) from aktualnosci into mid;
 elsif TG_TABLE_NAME = 'ekspozycje' then
    select coalesce(max(id),0) from ekspozycje into mid;
 elsif TG_TABLE_NAME = 'fakty' then
    select coalesce(max(id),0) from fakty into mid;
 elsif TG_TABLE_NAME = 'gleby' then
    select coalesce(max(id),0) from gleby into mid;
 elsif TG_TABLE_NAME = 'karty' then
    select coalesce(max(id),0) from karty into mid;
 elsif TG_TABLE_NAME = 'informacje' then
    select coalesce(max(id),0) from informacje into mid;
 elsif TG_TABLE_NAME = 'lokalizacje' then
    select coalesce(max(id),0) from lokalizacje into mid;
 elsif TG_TABLE_NAME = 'obszary' then
    select coalesce(max(id),0) from obszary into mid;
 elsif TG_TABLE_NAME = 'polozenia' then
    select coalesce(max(id),0) from polozenia into mid;
 elsif TG_TABLE_NAME = 'wnioski' then
    select coalesce(max(id),0) from wnioski into mid;
 elsif TG_TABLE_NAME = 'zagrozenia' then
    select coalesce(max(id),0) from zagrozenia into mid;
 end if;
 NEW.id := mid+1;
 return NEW;
end;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION fun_new_id() OWNER TO milosz;

