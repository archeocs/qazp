CREATE TABLE zagrozenia -- zagrozenia
(
  id integer NOT NULL,
  stanowisko integer NOT NULL,
  istnieje character varying(1) NOT NULL DEFAULT 'N',
  stale character varying(1) null, -- literka N oznacza zagrozenie dorazne, null - nieokreslone
  ludzie character varying(1) null, -- literna N oznacza zagrozenie przez nature, T - przez ludzi, null nieokreslone
  prywatny character varying(1) null, -- uzytkownik prywatny
  spoleczny character varying(1) null, -- uzytkownik spoleczny
  uwagi character varying(255),
  CONSTRAINT pk_zagrozenia PRIMARY KEY (id),
  constraint fk_stanowisko_zagrozenia foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade
);

CREATE TABLE ZAGROZENIA(
    id integer not null,
    stanowisko integer not null,
    wystepowanie varchar(1) not null, -- istnieje / nie istnieje
    przyczyna varchar(1), -- ludzie / natura
    uzytkownik varchar(1), -- wypelniane jezeli przyczyna == ludzie: uzytkownik spoleczny / prywatny
    uwagi varchar(255),
    CONSTRAINT zagrozenia_pkey PRIMARY KEY (id),
    constraint zagrozenia_st_fkey foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade,
    CONSTRAINT check_wystepowanie CHECK (wystepowanie in ('I','N')),
    CONSTRAINT check_przyczyna CHECK (przyczyna in ('L','N')),
    CONSTRAINT check_uzytkownik CHECK (uzytkownik in ('S','P')),
    constraint unique_zagrozenia_st unique(id, stanowisko)
);
