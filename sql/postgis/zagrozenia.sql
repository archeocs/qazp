CREATE TABLE ZAGROZENIA(
    id integer not null,
    stanowisko integer not null,
    wystepowanie varchar(1) not null, -- istnieje / nie istnieje
    czas varchar(1), -- stale / dorazne
    przyczyna varchar(1), -- ludzie / natura
    uzytkownik varchar(1), -- wypelniane jezeli przyczyna == ludzie: uzytkownik spoleczny / prywatny
    uwagi varchar(255),
    CONSTRAINT zagrozenia_pkey PRIMARY KEY (id),
    constraint zagrozenia_st_fkey foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade,
    CONSTRAINT check_wystepowanie CHECK (wystepowanie in ('I','N')),
    CONSTRAINT check_przyczyna CHECK (przyczyna in ('L','N')),
    CONSTRAINT check_uzytkownik CHECK (uzytkownik in ('S','P')),
    CONSTRAINT check_czas CHECK (czas in ('S','D')),
    constraint unique_zagrozenia_st unique(id, stanowisko)
);
