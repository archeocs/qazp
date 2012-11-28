-- drop table okresy_dziejow;
CREATE TABLE okresy_dziejow
( 
    kod varchar(4), 
    kod_epoka varchar(1), 
    epoka varchar(20), 
    okres varchar(20),  
    skrot varchar(20), 
    constraint okresy_dziejow_pkey primary key (kod)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE okresy_dziejow OWNER TO milosz;
insert into okresy_dziejow values('P', 'P', 'EPOKA KAMIENIA', NULL, 'EP. KAMIENIA');
insert into okresy_dziejow values('PP', 'P', 'EPOKA KAMIENIA', 'PALEOLIT', 'PALEOLIT');
insert into okresy_dziejow values('PM', 'P', 'EPOKA KAMIENIA', 'MEZOLIT', 'MEZOLIT');
insert into okresy_dziejow values('PL', 'P', 'EPOKA KAMIENIA', 'MEZOLIT/NEOLIT', 'MEZ/NEO');
insert into okresy_dziejow values('PN', 'P', 'EPOKA KAMIENIA', 'NEOLIT', 'NEOLIT');
insert into okresy_dziejow values('B', 'B', 'EPOKA BRĄZU', NULL, 'EP. BRĄZU');
insert into okresy_dziejow values('BW', 'B', 'EPOKA BRĄZU', 'WCZESNA', 'WCZESNY BRĄZ');
insert into okresy_dziejow values('BS', 'B', 'EPOKA BRĄZU', 'STARSZA', 'ST. EP. BRĄZU');
insert into okresy_dziejow values('BT', 'B', 'EPOKA BRĄZU', 'ŚRODKOWA', 'ŚROD. EP. BRĄZU');
insert into okresy_dziejow values('BM', 'B', 'EPOKA BRĄZU', 'MŁODSZA', 'MŁ. EP. BRĄZU');
insert into okresy_dziejow values('BP', 'B', 'EPOKA BRĄZU', 'PÓŹNA', 'PÓŹNY BRĄZ');
insert into okresy_dziejow values('B1', 'B', 'EPOKA BRĄZU', 'I', 'I EB');
insert into okresy_dziejow values('B2', 'B', 'EPOKA BRĄZU', 'II', 'II EB');
insert into okresy_dziejow values('B3', 'B', 'EPOKA BRĄZU', 'III', 'III EB');
insert into okresy_dziejow values('B4', 'B', 'EPOKA BRĄZU', 'IV', 'IV EB');
insert into okresy_dziejow values('B5', 'B', 'EPOKA BRĄZU', 'V', 'V EB');
insert into okresy_dziejow values('BA', 'B', 'EPOKA BRĄZU', 'A', 'EB A');
insert into okresy_dziejow values('BB', 'B', 'EPOKA BRĄZU', 'B', 'EB B');
insert into okresy_dziejow values('BC', 'B', 'EPOKA BRĄZU', 'C', 'EB C');
insert into okresy_dziejow values('BD', 'B', 'EPOKA BRĄZU', 'D', 'EB D');
insert into okresy_dziejow values('BH', 'B', 'EPOKA BRĄZU', 'OKRES HALSZTACKI', 'HALSZTACKI');
insert into okresy_dziejow values('BL', 'B', 'EPOKA BRĄZU', 'OKRES HALSZTACKI A', 'HA A');
insert into okresy_dziejow values('BN', 'B', 'EPOKA BRĄZU', 'OKRES HALSZTACKI B', 'HA B');
insert into okresy_dziejow values('Z', 'Z', 'EPOKA ŻELAZA', NULL, 'EP. ŻELAZA');
insert into okresy_dziejow values('ZW', 'Z', 'EPOKA ŻELAZA', 'WCZESNA', 'WCZES. EP. ŻELAZA');
insert into okresy_dziejow values('Z6', 'Z', 'EPOKA ŻELAZA', 'VI', 'EB VI');
insert into okresy_dziejow values('ZH', 'Z', 'EPOKA ŻELAZA', 'OKRES HALSZTACKI', 'HALSZTACKI');
insert into okresy_dziejow values('ZC', 'Z', 'EPOKA ŻELAZA', 'OKRES HALSZTACKI C', 'HA C');
insert into okresy_dziejow values('ZD', 'Z', 'EPOKA ŻELAZA', 'OKRES HALSZTACKI D', 'HA D');
insert into okresy_dziejow values('ZP', 'Z', 'EPOKA ŻELAZA', 'OKRES PRZEDRZYMSKI/LATEŃSKI', 'LATEŃSKI');
insert into okresy_dziejow values('ZR', 'Z', 'EPOKA ŻELAZA', 'OKRES WPŁYWÓW RZYMSKICH', 'OWR');
insert into okresy_dziejow values('ZL', 'Z', 'EPOKA ŻELAZA', 'OKRES WĘDRÓWEK LUDÓW', 'OWL');
insert into okresy_dziejow values('S', 'S', 'ŚREDNIOWIECZE', NULL, 'ŚREDNIOWIECZE');
insert into okresy_dziejow values('SW', 'S', 'ŚREDNIOWIECZE', 'WCZESNE', 'WCZES. ŚRED.');
insert into okresy_dziejow values('SP', 'S', 'ŚREDNIOWIECZE', 'PÓŹNE', 'PÓŹNE ŚRED.');
insert into okresy_dziejow values('N', 'N', 'NOWOŻYTNOŚĆ', NULL, 'NOWOŻYTNOŚĆ');
insert into okresy_dziejow values('XW', 'X', 'NOWOŻYTNOŚĆ', 'WCZESNA', 'WCZES. NOWOŻYT.');
insert into okresy_dziejow values('XP', 'X', 'NOWOŻYTNOŚĆ', 'PÓŹNA', 'PÓŻNA NOWOŻYT.');
insert into okresy_dziejow values('Y', 'Y', 'WSPÓŁCZESNOŚĆ', NULL, 'WSPÓŁCZESNOŚĆ');
insert into okresy_dziejow values('A', 'A', 'PRADZIEJE', NULL, 'PRADZIEJE');
