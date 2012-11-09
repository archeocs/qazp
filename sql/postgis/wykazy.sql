CREATE TABLE miejscowosci
(
    id integer primary key, 
    start varchar(2) not null, 
    nazwa varchar(50)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE miejscowosci OWNER TO milosz;

CREATE TABLE gminy
(
    id integer primary key, 
    start varchar(2) not null, 
    nazwa varchar(50)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE gminy OWNER TO milosz;

CREATE TABLE powiaty
(
    id integer primary key, 
    start varchar(2) not null, 
    nazwa varchar(50)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE powiaty OWNER TO milosz;

CREATE TABLE wojewodztwa
(
    id integer primary key, 
    start varchar(2) not null, 
    nazwa varchar(50)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE wojewodztwa OWNER TO milosz;
