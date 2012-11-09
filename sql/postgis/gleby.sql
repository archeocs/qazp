-- drop table gleby
CREATE TABLE gleby -- gleby 
(
  id integer NOT NULL,
  stanowisko integer NOT NULL,
  piaszczysta character varying(1) not null default 'N',
  gliniasta character varying(1) not null default 'N',
  bagnista character varying(1) not null default 'N',
  kamienistosc character varying(1) null, -- Mala, Srednia, Duza
  uwagi character varying(255) null,
  CONSTRAINT pk_gleby PRIMARY KEY (id),
  constraint fk_stanowisko_gleby foreign key (stanowisko) references stanowiska (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE cascade
);