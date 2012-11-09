drop table funkcje;
CREATE TABLE funkcje
(
 kod varchar(8) not null, 
 funkcja varchar(20), 
 czlon1 varchar(40), 
 czlon2 varchar(40), 
 czlon3 varchar(60), 
 nazwa varchar(110), 
 skrot varchar(20),
 constraint funkcje_pkey primary key(kod)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE miejsca OWNER TO milosz;

INSERT INTO funkcje VALUES('OT01','O','FORTALICJA',NULL,NULL,'FORTALICJA','FORTALICJA');
INSERT INTO funkcje VALUES('OF','O','FORTYFIKACJE',NULL,NULL,'FORTYFIKACJE','FORYFIK.');
INSERT INTO funkcje VALUES('OF01','O','FORTYFIKACJE','STAŁE',NULL,'FORTYFIKACJE STAŁE','FORYFIK.');
INSERT INTO funkcje VALUES('OF02','O','FORTYFIKACJE','POLOWE',NULL,'FORTYFIKACJE POLOWE','FORYFIK.');
INSERT INTO funkcje VALUES('OG','O','GRODZISKO',NULL,NULL,'GRODZISKO','GRODZ.');
INSERT INTO funkcje VALUES('OG01','O','GRODZISKO','CYPLOWE',NULL,'GRODZISKO CYPLOWE','GRODZ.');
INSERT INTO funkcje VALUES('OG02','O','GRODZISKO','STOŻKOWATE',NULL,'GRODZISKO STOŻKOWATE','GRODZ.');
INSERT INTO funkcje VALUES('OG03','O','GRODZISKO','PIERŚCIENIOWATE',NULL,'GRODZISKO PIERŚCIENIOWATE','GRODZ.');
INSERT INTO funkcje VALUES('BD','B','DEPOZYT',NULL,NULL,'DEPOZYT','DEPOZYT');
INSERT INTO funkcje VALUES('BG','B','GŁAZ NARZUTOWY',NULL,NULL,'GŁAZ NARZUTOWY','GŁAZ');
INSERT INTO funkcje VALUES('BS','B','KOŚCIÓŁ, ŚWIĄTYNIA, KAPLICA',NULL,NULL,'KOŚCIÓŁ, ŚWIĄTYNIA, KAPLICA','KOŚCIÓŁ');
INSERT INTO funkcje VALUES('BK','B','KRĄG KAMIENNY',NULL,NULL,'KRĄG KAMIENNY','KRĄG KAM.');
INSERT INTO funkcje VALUES('BM','B','MENHIR',NULL,NULL,'MENHIR','MENHIR');
INSERT INTO funkcje VALUES('BL','B','MIEJSCE KULTU',NULL,NULL,'MIEJSCE KULTU','MIEJ. KULT.');
INSERT INTO funkcje VALUES('BO01','B','MIEJSCE OFIARNE','LĄDOWE',NULL,'MIEJSCE OFIARNE LĄDOWE','MIEJ. OFI.');
INSERT INTO funkcje VALUES('BO02','B','MIEJSCE OFIARNE','BAGIENNE/WODNE',NULL,'MIEJSCE OFIARNE BAGIENNE/WODNE','MIEJ. OFI.');
INSERT INTO funkcje VALUES('BZ','B','POCHÓWEK ZWIERZĘCY',NULL,NULL,'POCHÓWEK ZWIERZĘCY','POCH. ZWI');
INSERT INTO funkcje VALUES('BR','B','ZAŁOŻENIE Z ROWAMI',NULL,NULL,'ZAŁOŻENIE Z ROWAMI','ZAŁ. Z ROW.');
INSERT INTO funkcje VALUES('BE','B','ZESPÓŁ KLASZTORNY/EREMICKI',NULL,NULL,'ZESPÓŁ KLASZTORNY/EREMICKI','ZESP KLASZ.');
INSERT INTO funkcje VALUES('MD','M','DWÓR',NULL,NULL,'DWÓR','DWÓR');
INSERT INTO funkcje VALUES('MF','M','FOLWARK',NULL,NULL,'FOLWARK','FOLWARK');
INSERT INTO funkcje VALUES('MJ','M','JASKINIA',NULL,NULL,'JASKINIA','JASKI.');
INSERT INTO funkcje VALUES('MU','M','JURYDYKA',NULL,NULL,'JURYDYKA','JURYDYK.');
INSERT INTO funkcje VALUES('MM','M','MIASTO',NULL,NULL,'MIASTO','MIASTO');
INSERT INTO funkcje VALUES('MO','M','OBOZOWISKO',NULL,NULL,'OBOZOWISKO','OBOZ.');
INSERT INTO funkcje VALUES('MO01','M','OBOZOWISKO','PODSTAWOWE',NULL,'OBOZOWISKO PODSTAWOWE','OBOZ.');
INSERT INTO funkcje VALUES('MO02','M','OBOZOWISKO','PUNKT ETAPOWY',NULL,'OBOZOWISKO PUNKT ETAPOWY','OBOZ.');
INSERT INTO funkcje VALUES('MO03','M','OBOZOWISKO','SPECJALNE/ FUNKCJONALNE',NULL,'OBOZOWISKO SPECJALNE/ FUNKCJONALNE','OBOZ.');
INSERT INTO funkcje VALUES('MS','M','OSADA',NULL,NULL,'OSADA','OSADA');
INSERT INTO funkcje VALUES('MS01','M','OSADA','NAWODNA/PALAFIT',NULL,'OSADA NAWODNA/PALAFIT','OSADA');
INSERT INTO funkcje VALUES('MS02','M','OSADA','O',NULL,'OSADA O','OSADA');
INSERT INTO funkcje VALUES('MS03','M','OSADA','PRZYGRODOWA',NULL,'OSADA PRZYGRODOWA','OSADA');
INSERT INTO funkcje VALUES('MS04','M','OSADA','OTOCZONA ROWEM/ROWAMI',NULL,'OSADA OTOCZONA ROWEM/ROWAMI','OSADA');
INSERT INTO funkcje VALUES('MS05','M','OSADA','OTWARTA',NULL,'OSADA OTWARTA','OSADA');
INSERT INTO funkcje VALUES('MS06','M','OSADA','WIEŚ',NULL,'OSADA WIEŚ','OSADA');
INSERT INTO funkcje VALUES('MS07','M','OSADA','INNA',NULL,'OSADA INNA','OSADA');
INSERT INTO funkcje VALUES('MP','M','PAŁAC',NULL,NULL,'PAŁAC','PAŁAC');
INSERT INTO funkcje VALUES('MR','M','PARK',NULL,NULL,'PARK','PARK');
INSERT INTO funkcje VALUES('MN','M','PUNKT OSADNICZY',NULL,NULL,'PUNKT OSADNICZY','PKT. OSAD');
INSERT INTO funkcje VALUES('MA','M','RELIKTY ARCHITEKTURY',NULL,NULL,'RELIKTY ARCHITEKTURY','REL. ARCH.');
INSERT INTO funkcje VALUES('MC','M','SCHRONISKO SKALNE',NULL,NULL,'SCHRONISKO SKALNE','SCHR. SKAL');
INSERT INTO funkcje VALUES('ML','M','ŚLAD OSADNICZY',NULL,NULL,'ŚLAD OSADNICZY','ŚL. OSAD');
INSERT INTO funkcje VALUES('MZ','M','ZAMEK',NULL,NULL,'ZAMEK','ZAMEK');
INSERT INTO funkcje VALUES('S','S',NULL,NULL,NULL,NULL,'SEPULK.');
INSERT INTO funkcje VALUES('SB','S','GRÓB BIRYTUALNY',NULL,NULL,'GRÓB BIRYTUALNY','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB01B','S','GRÓB BIRYTUALNY','KURHAN','BEZ NASYPU','GRÓB BIRYTUALNY KURHAN  BEZ NASYPU','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB01K','S','GRÓB BIRYTUALNY','KURHAN','Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','GRÓB BIRYTUALNY KURHAN  Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB01P','S','GRÓB BIRYTUALNY','KURHAN','Z PŁASZCZEM KAMIENNYM','GRÓB BIRYTUALNY KURHAN  Z PŁASZCZEM KAMIENNYM','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB01N','S','GRÓB BIRYTUALNY','KURHAN','Z ZACHOWANYM NASYPEM','GRÓB BIRYTUALNY KURHAN  Z ZACHOWANYM NASYPEM','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB02','S','GRÓB BIRYTUALNY','MEGAKSYLON',NULL,'GRÓB BIRYTUALNY MEGAKSYLON','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB03D','S','GRÓB BIRYTUALNY','MEGALIT','DOLMEN','GRÓB BIRYTUALNY MEGALIT DOLMEN','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB03G','S','GRÓB BIRYTUALNY','MEGALIT','GALERIOWY','GRÓB BIRYTUALNY MEGALIT GALERIOWY','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB03O','S','GRÓB BIRYTUALNY','MEGALIT','KORYTARZOWY','GRÓB BIRYTUALNY MEGALIT KORYTARZOWY','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB03Q','S','GRÓB BIRYTUALNY','MEGALIT','QUASI-MEGALIT','GRÓB BIRYTUALNY MEGALIT QUASI-MEGALIT','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB03S','S','GRÓB BIRYTUALNY','MEGALIT','SKRZYNKOWY','GRÓB BIRYTUALNY MEGALIT SKRZYNKOWY','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB03U','S','GRÓB BIRYTUALNY','MEGALIT','TYPU KUJAWSKIEGO','GRÓB BIRYTUALNY MEGALIT TYPU KUJAWSKIEGO','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB04','S','GRÓB BIRYTUALNY','NISZOWY/ KATAKUMBOWY',NULL,'GRÓB BIRYTUALNY NISZOWY/ KATAKUMBOWY','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB05S','S','GRÓB BIRYTUALNY','PŁASKI','SKRZYNKOWY','GRÓB BIRYTUALNY PŁASKI SKRZYNKOWY','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB05K','S','GRÓB BIRYTUALNY','PŁASKI','W OBSTAWIE KAMIENNEJ','GRÓB BIRYTUALNY PŁASKI W OBSTAWIE KAMIENNEJ','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB05W','S','GRÓB BIRYTUALNY','PŁASKI','WARSTWOWY','GRÓB BIRYTUALNY PŁASKI WARSTWOWY','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB05I','S','GRÓB BIRYTUALNY','PŁASKI','INNY','GRÓB BIRYTUALNY PŁASKI INNY','GRÓB BIR.');
INSERT INTO funkcje VALUES('SB06','S','GRÓB BIRYTUALNY','INNY',NULL,'GRÓB BIRYTUALNY INNY','GRÓB BIR.');
INSERT INTO funkcje VALUES('SR','S','CMENTARZYSKO BIRYTUALNE',NULL,NULL,'CMENTARZYSKO BIRYTUALNE','CM. BIR.');
INSERT INTO funkcje VALUES('SR01B','S','CMENTARZYSKO BIRYTUALNE','KURHANOWE','BEZ NASYPÓW','CMENTARZYSKO BIRYTUALNE KURHANOWE BEZ NASYPÓW','CM. BIR.');
INSERT INTO funkcje VALUES('SR01K','S','CMENTARZYSKO BIRYTUALNE','KURHANOWE','Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','CMENTARZYSKO BIRYTUALNE KURHANOWE Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','CM. BIR.');
INSERT INTO funkcje VALUES('SR01P','S','CMENTARZYSKO BIRYTUALNE','KURHANOWE','Z PŁASZCZEM KAMIENNYM','CMENTARZYSKO BIRYTUALNE KURHANOWE Z PŁASZCZEM KAMIENNYM','CM. BIR.');
INSERT INTO funkcje VALUES('SR01N','S','CMENTARZYSKO BIRYTUALNE','KURHANOWE','Z ZACHOWANYMI NASYPAMI','CMENTARZYSKO BIRYTUALNE KURHANOWE Z ZACHOWANYMI NASYPAMI','CM. BIR.');
INSERT INTO funkcje VALUES('SR02D','S','CMENTARZYSKO BIRYTUALNE','MEGALITYCZNE','DOLMENY','CMENTARZYSKO BIRYTUALNE MEGALITYCZNE DOLMENY','CM. BIR.');
INSERT INTO funkcje VALUES('SR02G','S','CMENTARZYSKO BIRYTUALNE','MEGALITYCZNE','MEGALITY GALERIOWE','CMENTARZYSKO BIRYTUALNE MEGALITYCZNE MEGALITY GALERIOWE','CM. BIR.');
INSERT INTO funkcje VALUES('SR02O','S','CMENTARZYSKO BIRYTUALNE','MEGALITYCZNE','MEGALITY KORYTARZOWE','CMENTARZYSKO BIRYTUALNE MEGALITYCZNE MEGALITY KORYTARZOWE','CM. BIR.');
INSERT INTO funkcje VALUES('SR02S','S','CMENTARZYSKO BIRYTUALNE','MEGALITYCZNE','MEGALITY SKRZYNKOWE','CMENTARZYSKO BIRYTUALNE MEGALITYCZNE MEGALITY SKRZYNKOWE','CM. BIR.');
INSERT INTO funkcje VALUES('SR02U','S','CMENTARZYSKO BIRYTUALNE','MEGALITYCZNE','MEGALITY TYPU KUJAWSKIEGO','CMENTARZYSKO BIRYTUALNE MEGALITYCZNE MEGALITY TYPU KUJAWSKIEGO','CM. BIR.');
INSERT INTO funkcje VALUES('SR02Q','S','CMENTARZYSKO BIRYTUALNE','MEGALITYCZNE','QUASI-MEGALITY','CMENTARZYSKO BIRYTUALNE MEGALITYCZNE QUASI-MEGALITY','CM. BIR.');
INSERT INTO funkcje VALUES('SR03S','S','CMENTARZYSKO BIRYTUALNE','PŁASKIE','GROBY SKRZYNKOWE','CMENTARZYSKO BIRYTUALNE PŁASKIE GROBY SKRZYNKOWE','CM. BIR.');
INSERT INTO funkcje VALUES('SR03K','S','CMENTARZYSKO BIRYTUALNE','PŁASKIE','GROBY W OBSTAWIE KAMIENNEJ','CMENTARZYSKO BIRYTUALNE PŁASKIE GROBY W OBSTAWIE KAMIENNEJ','CM. BIR.');
INSERT INTO funkcje VALUES('SR03W','S','CMENTARZYSKO BIRYTUALNE','PŁASKIE','GROBY WARSTWOWE','CMENTARZYSKO BIRYTUALNE PŁASKIE GROBY WARSTWOWE','CM. BIR.');
INSERT INTO funkcje VALUES('SR03I','S','CMENTARZYSKO BIRYTUALNE','PŁASKIE','INNE','CMENTARZYSKO BIRYTUALNE PŁASKIE INNE','CM. BIR.');
INSERT INTO funkcje VALUES('SR04','S','CMENTARZYSKO BIRYTUALNE','INNE',NULL,'CMENTARZYSKO BIRYTUALNE INNE','CM. BIR.');
INSERT INTO funkcje VALUES('SS','S','GRÓB SZKIELETOWY',NULL,NULL,'GRÓB SZKIELETOWY','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS01B','S','GRÓB SZKIELETOWY','KURHAN','BEZ NASYPU','GRÓB SZKIELETOWY KURHAN  BEZ NASYPU','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS01K','S','GRÓB SZKIELETOWY','KURHAN','Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','GRÓB SZKIELETOWY KURHAN  Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS01P','S','GRÓB SZKIELETOWY','KURHAN','Z PŁASZCZEM KAMIENNYM','GRÓB SZKIELETOWY KURHAN  Z PŁASZCZEM KAMIENNYM','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS01N','S','GRÓB SZKIELETOWY','KURHAN','Z ZACHOWANYM NASYPEM','GRÓB SZKIELETOWY KURHAN  Z ZACHOWANYM NASYPEM','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS02','S','GRÓB SZKIELETOWY','MEGAKSYLON',NULL,'GRÓB SZKIELETOWY MEGAKSYLON','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS03D','S','GRÓB SZKIELETOWY','MEGALIT','DOLMEN','GRÓB SZKIELETOWY MEGALIT DOLMEN','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS03G','S','GRÓB SZKIELETOWY','MEGALIT','GALERIOWY','GRÓB SZKIELETOWY MEGALIT GALERIOWY','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS03O','S','GRÓB SZKIELETOWY','MEGALIT','KORYTARZOWY','GRÓB SZKIELETOWY MEGALIT KORYTARZOWY','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS03Q','S','GRÓB SZKIELETOWY','MEGALIT','QUASI-MEGALIT','GRÓB SZKIELETOWY MEGALIT QUASI-MEGALIT','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS03S','S','GRÓB SZKIELETOWY','MEGALIT','SKRZYNKOWY','GRÓB SZKIELETOWY MEGALIT SKRZYNKOWY','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS03U','S','GRÓB SZKIELETOWY','MEGALIT','TYPU KUJAWSKIEGO','GRÓB SZKIELETOWY MEGALIT TYPU KUJAWSKIEGO','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS04','S','GRÓB SZKIELETOWY','NISZOWY/ KATAKUMBOWY',NULL,'GRÓB SZKIELETOWY NISZOWY/ KATAKUMBOWY','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS05S','S','GRÓB SZKIELETOWY','PŁASKI','SKRZYNKOWY','GRÓB SZKIELETOWY PŁASKI SKRZYNKOWY','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS05K','S','GRÓB SZKIELETOWY','PŁASKI','W OBSTAWIE KAMIENNEJ','GRÓB SZKIELETOWY PŁASKI W OBSTAWIE KAMIENNEJ','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS05I','S','GRÓB SZKIELETOWY','PŁASKI','INNY','GRÓB SZKIELETOWY PŁASKI INNY','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SS06','S','GRÓB SZKIELETOWY','INNY',NULL,'GRÓB SZKIELETOWY INNY','GRÓB. SZK.');
INSERT INTO funkcje VALUES('SZ','S','CMENTARZYSKO SZKIELETOWE',NULL,NULL,'CMENTARZYSKO SZKIELETOWE','CM. SZK.');
INSERT INTO funkcje VALUES('SZ01B','S','CMENTARZYSKO SZKIELETOWE','KURHANOWE','BEZ NASYPÓW','CMENTARZYSKO SZKIELETOWE KURHANOWE BEZ NASYPÓW','CM. SZK.');
INSERT INTO funkcje VALUES('SZ01K','S','CMENTARZYSKO SZKIELETOWE','KURHANOWE','Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','CMENTARZYSKO SZKIELETOWE KURHANOWE Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','CM. SZK.');
INSERT INTO funkcje VALUES('SZ01P','S','CMENTARZYSKO SZKIELETOWE','KURHANOWE','Z PŁASZCZEM KAMIENNYM','CMENTARZYSKO SZKIELETOWE KURHANOWE Z PŁASZCZEM KAMIENNYM','CM. SZK.');
INSERT INTO funkcje VALUES('SZ01N','S','CMENTARZYSKO SZKIELETOWE','KURHANOWE','Z ZACHOWANYMI NASYPAMI','CMENTARZYSKO SZKIELETOWE KURHANOWE Z ZACHOWANYMI NASYPAMI','CM. SZK.');
INSERT INTO funkcje VALUES('SZ02D','S','CMENTARZYSKO SZKIELETOWE','MEGALITYCZNE','DOLMENY','CMENTARZYSKO SZKIELETOWE MEGALITYCZNE DOLMENY','CM. SZK.');
INSERT INTO funkcje VALUES('SZ02G','S','CMENTARZYSKO SZKIELETOWE','MEGALITYCZNE','MEGALITY GALERIOWE','CMENTARZYSKO SZKIELETOWE MEGALITYCZNE MEGALITY GALERIOWE','CM. SZK.');
INSERT INTO funkcje VALUES('SZ02O','S','CMENTARZYSKO SZKIELETOWE','MEGALITYCZNE','MEGALITY KORYTARZOWE','CMENTARZYSKO SZKIELETOWE MEGALITYCZNE MEGALITY KORYTARZOWE','CM. SZK.');
INSERT INTO funkcje VALUES('SZ02S','S','CMENTARZYSKO SZKIELETOWE','MEGALITYCZNE','MEGALITY SKRZYNKOWE','CMENTARZYSKO SZKIELETOWE MEGALITYCZNE MEGALITY SKRZYNKOWE','CM. SZK.');
INSERT INTO funkcje VALUES('SZ02U','S','CMENTARZYSKO SZKIELETOWE','MEGALITYCZNE','MEGALITY TYPU KUJAWSKIEGO','CMENTARZYSKO SZKIELETOWE MEGALITYCZNE MEGALITY TYPU KUJAWSKIEGO','CM. SZK.');
INSERT INTO funkcje VALUES('SZ02Q','S','CMENTARZYSKO SZKIELETOWE','MEGALITYCZNE','QUASI-MEGALITY','CMENTARZYSKO SZKIELETOWE MEGALITYCZNE QUASI-MEGALITY','CM. SZK.');
INSERT INTO funkcje VALUES('SZ03S','S','CMENTARZYSKO SZKIELETOWE','PŁASKIE','GROBY SKRZYNKOWE','CMENTARZYSKO SZKIELETOWE PŁASKIE GROBY SKRZYNKOWE','CM. SZK.');
INSERT INTO funkcje VALUES('SZ03K','S','CMENTARZYSKO SZKIELETOWE','PŁASKIE','GROBY W OBSTAWIE KAMIENNEJ','CMENTARZYSKO SZKIELETOWE PŁASKIE GROBY W OBSTAWIE KAMIENNEJ','CM. SZK.');
INSERT INTO funkcje VALUES('SZ03W','S','CMENTARZYSKO SZKIELETOWE','PŁASKIE','GROBY WARSTWOWE','CMENTARZYSKO SZKIELETOWE PŁASKIE GROBY WARSTWOWE','CM. SZK.');
INSERT INTO funkcje VALUES('SZ03I','S','CMENTARZYSKO SZKIELETOWE','PŁASKIE','INNE','CMENTARZYSKO SZKIELETOWE PŁASKIE INNE','CM. SZK.');
INSERT INTO funkcje VALUES('SZ04','S','CMENTARZYSKO SZKIELETOWE','INNE',NULL,'CMENTARZYSKO SZKIELETOWE INNE','CM. SZK.');
INSERT INTO funkcje VALUES('SP','S','GRÓB CIAŁOPALNY',NULL,NULL,'GRÓB CIAŁOPALNY','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP01B','S','GRÓB CIAŁOPALNY','KURHAN','BEZ NASYPU','GRÓB CIAŁOPALNY KURHAN  BEZ NASYPU','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP01K','S','GRÓB CIAŁOPALNY','KURHAN','Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','GRÓB CIAŁOPALNY KURHAN  Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP01P','S','GRÓB CIAŁOPALNY','KURHAN','Z PŁASZCZEM KAMIENNYM','GRÓB CIAŁOPALNY KURHAN  Z PŁASZCZEM KAMIENNYM','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP01N','S','GRÓB CIAŁOPALNY','KURHAN','Z ZACHOWANYM NASYPEM','GRÓB CIAŁOPALNY KURHAN  Z ZACHOWANYM NASYPEM','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP02','S','GRÓB CIAŁOPALNY','MEGAKSYLON',NULL,'GRÓB CIAŁOPALNY MEGAKSYLON','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP03D','S','GRÓB CIAŁOPALNY','MEGALIT','DOLMEN','GRÓB CIAŁOPALNY MEGALIT DOLMEN','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP03G','S','GRÓB CIAŁOPALNY','MEGALIT','GALERIOWY','GRÓB CIAŁOPALNY MEGALIT GALERIOWY','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP03O','S','GRÓB CIAŁOPALNY','MEGALIT','KORYTARZOWY','GRÓB CIAŁOPALNY MEGALIT KORYTARZOWY','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP03Q','S','GRÓB CIAŁOPALNY','MEGALIT','QUASI-MEGALIT','GRÓB CIAŁOPALNY MEGALIT QUASI-MEGALIT','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP03S','S','GRÓB CIAŁOPALNY','MEGALIT','SKRZYNKOWY','GRÓB CIAŁOPALNY MEGALIT SKRZYNKOWY','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP03U','S','GRÓB CIAŁOPALNY','MEGALIT','TYPU KUJAWSKIEGO','GRÓB CIAŁOPALNY MEGALIT TYPU KUJAWSKIEGO','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP04','S','GRÓB CIAŁOPALNY','NISZOWY/ KATAKUMBOWY',NULL,'GRÓB CIAŁOPALNY NISZOWY/ KATAKUMBOWY','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP05J','S','GRÓB CIAŁOPALNY','PŁASKI','JAMOWY','GRÓB CIAŁOPALNY PŁASKI JAMOWY','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP05P','S','GRÓB CIAŁOPALNY','PŁASKI','POPIELNICOWY','GRÓB CIAŁOPALNY PŁASKI POPIELNICOWY','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP05S','S','GRÓB CIAŁOPALNY','PŁASKI','SKRZYNKOWY','GRÓB CIAŁOPALNY PŁASKI SKRZYNKOWY','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP05K','S','GRÓB CIAŁOPALNY','PŁASKI','W OBSTAWIE KAMIENNEJ','GRÓB CIAŁOPALNY PŁASKI W OBSTAWIE KAMIENNEJ','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP05W','S','GRÓB CIAŁOPALNY','PŁASKI','WARSTWOWY','GRÓB CIAŁOPALNY PŁASKI WARSTWOWY','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP05I','S','GRÓB CIAŁOPALNY','PŁASKI','INNY','GRÓB CIAŁOPALNY PŁASKI INNY','GRÓB CIA.');
INSERT INTO funkcje VALUES('SP06','S','GRÓB CIAŁOPALNY','INNY',NULL,'GRÓB CIAŁOPALNY INNY','GRÓB CIA.');
INSERT INTO funkcje VALUES('SL','S','CMENTARZYSKO CIAŁOPALNE',NULL,NULL,'CMENTARZYSKO CIAŁOPALNE','CM. CIA.');
INSERT INTO funkcje VALUES('SL01B','S','CMENTARZYSKO CIAŁOPALNE','KURHANOWE','BEZ NASYPÓW','CMENTARZYSKO CIAŁOPALNE KURHANOWE BEZ NASYPÓW','CM. CIA.');
INSERT INTO funkcje VALUES('SL01K','S','CMENTARZYSKO CIAŁOPALNE','KURHANOWE','Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','CMENTARZYSKO CIAŁOPALNE KURHANOWE Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','CM. CIA.');
INSERT INTO funkcje VALUES('SL01P','S','CMENTARZYSKO CIAŁOPALNE','KURHANOWE','Z PŁASZCZEM KAMIENNYM','CMENTARZYSKO CIAŁOPALNE KURHANOWE Z PŁASZCZEM KAMIENNYM','CM. CIA.');
INSERT INTO funkcje VALUES('SL01N','S','CMENTARZYSKO CIAŁOPALNE','KURHANOWE','Z ZACHOWANYMI NASYPAMI','CMENTARZYSKO CIAŁOPALNE KURHANOWE Z ZACHOWANYMI NASYPAMI','CM. CIA.');
INSERT INTO funkcje VALUES('SL02D','S','CMENTARZYSKO CIAŁOPALNE','MEGALITYCZNE','DOLMENY','CMENTARZYSKO CIAŁOPALNE MEGALITYCZNE DOLMENY','CM. CIA.');
INSERT INTO funkcje VALUES('SL02G','S','CMENTARZYSKO CIAŁOPALNE','MEGALITYCZNE','MEGALITY GALERIOWE','CMENTARZYSKO CIAŁOPALNE MEGALITYCZNE MEGALITY GALERIOWE','CM. CIA.');
INSERT INTO funkcje VALUES('SL02O','S','CMENTARZYSKO CIAŁOPALNE','MEGALITYCZNE','MEGALITY KORYTARZOWE','CMENTARZYSKO CIAŁOPALNE MEGALITYCZNE MEGALITY KORYTARZOWE','CM. CIA.');
INSERT INTO funkcje VALUES('SL02S','S','CMENTARZYSKO CIAŁOPALNE','MEGALITYCZNE','MEGALITY SKRZYNKOWE','CMENTARZYSKO CIAŁOPALNE MEGALITYCZNE MEGALITY SKRZYNKOWE','CM. CIA.');
INSERT INTO funkcje VALUES('SL02U','S','CMENTARZYSKO CIAŁOPALNE','MEGALITYCZNE','MEGALITY TYPU KUJAWSKIEGO','CMENTARZYSKO CIAŁOPALNE MEGALITYCZNE MEGALITY TYPU KUJAWSKIEGO','CM. CIA.');
INSERT INTO funkcje VALUES('SL02Q','S','CMENTARZYSKO CIAŁOPALNE','MEGALITYCZNE','QUASI-MEGALITY','CMENTARZYSKO CIAŁOPALNE MEGALITYCZNE QUASI-MEGALITY','CM. CIA.');
INSERT INTO funkcje VALUES('SL03J','S','CMENTARZYSKO CIAŁOPALNE','PŁASKIE','GROBY JAMOWE','CMENTARZYSKO CIAŁOPALNE PŁASKIE GROBY JAMOWE','CM. CIA.');
INSERT INTO funkcje VALUES('SL03P','S','CMENTARZYSKO CIAŁOPALNE','PŁASKIE','GROBY POPIELNICOWE','CMENTARZYSKO CIAŁOPALNE PŁASKIE GROBY POPIELNICOWE','CM. CIA.');
INSERT INTO funkcje VALUES('SL03S','S','CMENTARZYSKO CIAŁOPALNE','PŁASKIE','GROBY SKRZYNKOWE','CMENTARZYSKO CIAŁOPALNE PŁASKIE GROBY SKRZYNKOWE','CM. CIA.');
INSERT INTO funkcje VALUES('SL03K','S','CMENTARZYSKO CIAŁOPALNE','PŁASKIE','GROBY W OBSTAWIE KAMIENNEJ','CMENTARZYSKO CIAŁOPALNE PŁASKIE GROBY W OBSTAWIE KAMIENNEJ','CM. CIA.');
INSERT INTO funkcje VALUES('SL03W','S','CMENTARZYSKO CIAŁOPALNE','PŁASKIE','GROBY WARSTWOWE','CMENTARZYSKO CIAŁOPALNE PŁASKIE GROBY WARSTWOWE','CM. CIA.');
INSERT INTO funkcje VALUES('SL03I','S','CMENTARZYSKO CIAŁOPALNE','PŁASKIE','INNE','CMENTARZYSKO CIAŁOPALNE PŁASKIE INNE','CM. CIA.');
INSERT INTO funkcje VALUES('SL04','S','CMENTARZYSKO CIAŁOPALNE','INNE',NULL,'CMENTARZYSKO CIAŁOPALNE INNE','CM. CIA.');
INSERT INTO funkcje VALUES('SG','S','GRÓB',NULL,NULL,'GRÓB','GRÓB');
INSERT INTO funkcje VALUES('SG01B','S','GRÓB','KURHAN','BEZ NASYPU','GRÓB KURHAN  BEZ NASYPU','GRÓB');
INSERT INTO funkcje VALUES('SG01K','S','GRÓB','KURHAN','Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','GRÓB KURHAN  Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','GRÓB');
INSERT INTO funkcje VALUES('SG01P','S','GRÓB','KURHAN','Z PŁASZCZEM KAMIENNYM','GRÓB KURHAN  Z PŁASZCZEM KAMIENNYM','GRÓB');
INSERT INTO funkcje VALUES('SG01N','S','GRÓB','KURHAN','Z ZACHOWANYM NASYPEM','GRÓB KURHAN  Z ZACHOWANYM NASYPEM','GRÓB');
INSERT INTO funkcje VALUES('SG02','S','GRÓB','MEGAKSYLON',NULL,'GRÓB MEGAKSYLON','GRÓB');
INSERT INTO funkcje VALUES('SG03D','S','GRÓB','MEGALIT','DOLMEN','GRÓB MEGALIT DOLMEN','GRÓB');
INSERT INTO funkcje VALUES('SG03G','S','GRÓB','MEGALIT','GALERIOWY','GRÓB MEGALIT GALERIOWY','GRÓB');
INSERT INTO funkcje VALUES('SG03O','S','GRÓB','MEGALIT','KORYTARZOWY','GRÓB MEGALIT KORYTARZOWY','GRÓB');
INSERT INTO funkcje VALUES('SG03Q','S','GRÓB','MEGALIT','QUASI-MEGALIT','GRÓB MEGALIT QUASI-MEGALIT','GRÓB');
INSERT INTO funkcje VALUES('SG03S','S','GRÓB','MEGALIT','SKRZYNKOWY','GRÓB MEGALIT SKRZYNKOWY','GRÓB');
INSERT INTO funkcje VALUES('SG03U','S','GRÓB','MEGALIT','TYPU KUJAWSKIEGO','GRÓB MEGALIT TYPU KUJAWSKIEGO','GRÓB');
INSERT INTO funkcje VALUES('SG04','S','GRÓB','NISZOWY/ KATAKUMBOWY',NULL,'GRÓB NISZOWY/ KATAKUMBOWY','GRÓB');
INSERT INTO funkcje VALUES('SG05J','S','GRÓB','PŁASKI','JAMOWY','GRÓB PŁASKI JAMOWY','GRÓB');
INSERT INTO funkcje VALUES('SG05P','S','GRÓB','PŁASKI','POPIELNICOWY','GRÓB PŁASKI POPIELNICOWY','GRÓB');
INSERT INTO funkcje VALUES('SG05S','S','GRÓB','PŁASKI','SKRZYNKOWY','GRÓB PŁASKI SKRZYNKOWY','GRÓB');
INSERT INTO funkcje VALUES('SG05K','S','GRÓB','PŁASKI','W OBSTAWIE KAMIENNEJ','GRÓB PŁASKI W OBSTAWIE KAMIENNEJ','GRÓB');
INSERT INTO funkcje VALUES('SG05W','S','GRÓB','PŁASKI','WARSTWOWY','GRÓB PŁASKI WARSTWOWY','GRÓB');
INSERT INTO funkcje VALUES('SG05I','S','GRÓB','PŁASKI','INNY','GRÓB PŁASKI INNY','GRÓB');
INSERT INTO funkcje VALUES('SG06','S','GRÓB','INNY',NULL,'GRÓB INNY','GRÓB');
INSERT INTO funkcje VALUES('SC','S','CMENTARZYSKO',NULL,NULL,'CMENTARZYSKO','CMENT.');
INSERT INTO funkcje VALUES('SC01B','S','CMENTARZYSKO','KURHANOWE','BEZ NASYPÓW','CMENTARZYSKO KURHANOWE BEZ NASYPÓW','CMENT.');
INSERT INTO funkcje VALUES('SC01K','S','CMENTARZYSKO','KURHANOWE','Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','CMENTARZYSKO KURHANOWE Z KONSTRUKCJAMI KAMIENNYMI W CZĘŚCI PŁASKIEJ (KRĘGI, BRUKI)','CMENT.');
INSERT INTO funkcje VALUES('SC01P','S','CMENTARZYSKO','KURHANOWE','Z PŁASZCZEM KAMIENNYM','CMENTARZYSKO KURHANOWE Z PŁASZCZEM KAMIENNYM','CMENT.');
INSERT INTO funkcje VALUES('SC01N','S','CMENTARZYSKO','KURHANOWE','Z ZACHOWANYMI NASYPAMI','CMENTARZYSKO KURHANOWE Z ZACHOWANYMI NASYPAMI','CMENT.');
INSERT INTO funkcje VALUES('SC02D','S','CMENTARZYSKO','MEGALITYCZNE','DOLMENY','CMENTARZYSKO MEGALITYCZNE DOLMENY','CMENT.');
INSERT INTO funkcje VALUES('SC02G','S','CMENTARZYSKO','MEGALITYCZNE','MEGALITY GALERIOWE','CMENTARZYSKO MEGALITYCZNE MEGALITY GALERIOWE','CMENT.');
INSERT INTO funkcje VALUES('SC02O','S','CMENTARZYSKO','MEGALITYCZNE','MEGALITY KORYTARZOWE','CMENTARZYSKO MEGALITYCZNE MEGALITY KORYTARZOWE','CMENT.');
INSERT INTO funkcje VALUES('SC02S','S','CMENTARZYSKO','MEGALITYCZNE','MEGALITY SKRZYNKOWE','CMENTARZYSKO MEGALITYCZNE MEGALITY SKRZYNKOWE','CMENT.');
INSERT INTO funkcje VALUES('SC02U','S','CMENTARZYSKO','MEGALITYCZNE','MEGALITY TYPU KUJAWSKIEGO','CMENTARZYSKO MEGALITYCZNE MEGALITY TYPU KUJAWSKIEGO','CMENT.');
INSERT INTO funkcje VALUES('SC02Q','S','CMENTARZYSKO','MEGALITYCZNE','QUASI-MEGALITY','CMENTARZYSKO MEGALITYCZNE QUASI-MEGALITY','CMENT.');
INSERT INTO funkcje VALUES('SC03J','S','CMENTARZYSKO','PŁASKIE','GROBY JAMOWE','CMENTARZYSKO PŁASKIE GROBY JAMOWE','CMENT.');
INSERT INTO funkcje VALUES('SC03P','S','CMENTARZYSKO','PŁASKIE','GROBY POPIELNICOWE','CMENTARZYSKO PŁASKIE GROBY POPIELNICOWE','CMENT.');
INSERT INTO funkcje VALUES('SC03S','S','CMENTARZYSKO','PŁASKIE','GROBY SKRZYNKOWE','CMENTARZYSKO PŁASKIE GROBY SKRZYNKOWE','CMENT.');
INSERT INTO funkcje VALUES('SC03K','S','CMENTARZYSKO','PŁASKIE','GROBY W OBSTAWIE KAMIENNEJ','CMENTARZYSKO PŁASKIE GROBY W OBSTAWIE KAMIENNEJ','CMENT.');
INSERT INTO funkcje VALUES('SC03W','S','CMENTARZYSKO','PŁASKIE','GROBY WARSTWOWE','CMENTARZYSKO PŁASKIE GROBY WARSTWOWE','CMENT.');
INSERT INTO funkcje VALUES('SC03I','S','CMENTARZYSKO','PŁASKIE','INNE','CMENTARZYSKO PŁASKIE INNE','CMENT.');
INSERT INTO funkcje VALUES('SC04','S','CMENTARZYSKO','INNE',NULL,'CMENTARZYSKO INNE','CMENT.');
INSERT INTO funkcje VALUES('SN','S','NIEPOCHOWANE SZCZĄTKI LUDZKIE',NULL,NULL,'NIEPOCHOWANE SZCZĄTKI LUDZKIE','SZCZĄTKI');
INSERT INTO funkcje VALUES('G','G',NULL,NULL,NULL,NULL,'GOSP');
INSERT INTO funkcje VALUES('GI','G','INFRASTRUKTURA',NULL,NULL,'INFRASTRUKTURA','INFRASTR.');
INSERT INTO funkcje VALUES('GI01','G','INFRASTRUKTURA','BRÓD',NULL,'INFRASTRUKTURA BRÓD','INFRASTR.');
INSERT INTO funkcje VALUES('GI02','G','INFRASTRUKTURA','DROGA',NULL,'INFRASTRUKTURA DROGA','INFRASTR.');
INSERT INTO funkcje VALUES('GI03','G','INFRASTRUKTURA','FABRYKA',NULL,'INFRASTRUKTURA FABRYKA','INFRASTR.');
INSERT INTO funkcje VALUES('GI04','G','INFRASTRUKTURA','FALOCHRON',NULL,'INFRASTRUKTURA FALOCHRON','INFRASTR.');
INSERT INTO funkcje VALUES('GI05','G','INFRASTRUKTURA','GROBLA',NULL,'INFRASTRUKTURA GROBLA','INFRASTR.');
INSERT INTO funkcje VALUES('GI06','G','INFRASTRUKTURA','KANAŁ',NULL,'INFRASTRUKTURA KANAŁ','INFRASTR.');
INSERT INTO funkcje VALUES('GI07','G','INFRASTRUKTURA','KARCZMA',NULL,'INFRASTRUKTURA KARCZMA','INFRASTR.');
INSERT INTO funkcje VALUES('GI08','G','INFRASTRUKTURA','LATARNIA',NULL,'INFRASTRUKTURA LATARNIA','INFRASTR.');
INSERT INTO funkcje VALUES('GI09','G','INFRASTRUKTURA','MOST',NULL,'INFRASTRUKTURA MOST','INFRASTR.');
INSERT INTO funkcje VALUES('GI10','G','INFRASTRUKTURA','NABRZEŻE',NULL,'INFRASTRUKTURA NABRZEŻE','INFRASTR.');
INSERT INTO funkcje VALUES('GI11','G','INFRASTRUKTURA','POMOST',NULL,'INFRASTRUKTURA POMOST','INFRASTR.');
INSERT INTO funkcje VALUES('GI12','G','INFRASTRUKTURA','PORT',NULL,'INFRASTRUKTURA PORT','INFRASTR.');
INSERT INTO funkcje VALUES('GI13','G','INFRASTRUKTURA','STUDNIA',NULL,'INFRASTRUKTURA STUDNIA','INFRASTR.');
INSERT INTO funkcje VALUES('GI14','G','INFRASTRUKTURA','WODOCIĄGI I KANALIZACJA',NULL,'INFRASTRUKTURA WODOCIĄGI I KANALIZACJA','INFRASTR.');
INSERT INTO funkcje VALUES('GI15','G','INFRASTRUKTURA','INNE',NULL,'INFRASTRUKTURA INNE','INFRASTR.');
INSERT INTO funkcje VALUES('GK','G','KILL SITE',NULL,NULL,'KILL SITE','KILL SITE');
INSERT INTO funkcje VALUES('GZ','G','KRALL/ZAGRODA DLA ZWIERZĄT',NULL,NULL,'KRALL/ZAGRODA DLA ZWIERZĄT','KRALL');
INSERT INTO funkcje VALUES('GE','G','MIEJSCE EKSPLOATACJI SUROWCA',NULL,NULL,'MIEJSCE EKSPLOATACJI SUROWCA','MIEJ. EKSP.');
INSERT INTO funkcje VALUES('GE01','G','MIEJSCE EKSPLOATACJI SUROWCA','GLINIANKA',NULL,'MIEJSCE EKSPLOATACJI SUROWCA GLINIANKA','MIEJ. EKSP.');
INSERT INTO funkcje VALUES('GE02','G','MIEJSCE EKSPLOATACJI SUROWCA','KOPALNIA',NULL,'MIEJSCE EKSPLOATACJI SUROWCA KOPALNIA','MIEJ. EKSP.');
INSERT INTO funkcje VALUES('GE03','G','MIEJSCE EKSPLOATACJI SUROWCA','KOPALNIA KRZEMIENIA',NULL,'MIEJSCE EKSPLOATACJI SUROWCA KOPALNIA KRZEMIENIA','MIEJ. EKSP.');
INSERT INTO funkcje VALUES('GE04','G','MIEJSCE EKSPLOATACJI SUROWCA','INNE',NULL,'MIEJSCE EKSPLOATACJI SUROWCA INNE','MIEJ. EKSP.');
INSERT INTO funkcje VALUES('GP','G','MIEJSCE PRODUKCJI',NULL,NULL,'MIEJSCE PRODUKCJI','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP01','G','MIEJSCE PRODUKCJI','BROWAR',NULL,'MIEJSCE PRODUKCJI BROWAR','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP02','G','MIEJSCE PRODUKCJI','DYMARKI',NULL,'MIEJSCE PRODUKCJI DYMARKI','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP03','G','MIEJSCE PRODUKCJI','GARBARNIA',NULL,'MIEJSCE PRODUKCJI GARBARNIA','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP04','G','MIEJSCE PRODUKCJI','GARNCARNIA',NULL,'MIEJSCE PRODUKCJI GARNCARNIA','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP05','G','MIEJSCE PRODUKCJI','GORZELNIA',NULL,'MIEJSCE PRODUKCJI GORZELNIA','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP06','G','MIEJSCE PRODUKCJI','HUTA',NULL,'MIEJSCE PRODUKCJI HUTA','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP07','G','MIEJSCE PRODUKCJI','KRZEMIENICA',NULL,'MIEJSCE PRODUKCJI KRZEMIENICA','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP08','G','MIEJSCE PRODUKCJI','KUŹNIA',NULL,'MIEJSCE PRODUKCJI KUŹNIA','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP09','G','MIEJSCE PRODUKCJI','MANUFAKTURA',NULL,'MIEJSCE PRODUKCJI MANUFAKTURA','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP10','G','MIEJSCE PRODUKCJI','MIEJSCE OBRÓBKI SUROWCÓW',NULL,'MIEJSCE PRODUKCJI MIEJSCE OBRÓBKI SUROWCÓW','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP11','G','MIEJSCE PRODUKCJI','MIELERZ',NULL,'MIEJSCE PRODUKCJI MIELERZ','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP12','G','MIEJSCE PRODUKCJI','MŁYN',NULL,'MIEJSCE PRODUKCJI MŁYN','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP13','G','MIEJSCE PRODUKCJI','PIECOWISKO',NULL,'MIEJSCE PRODUKCJI PIECOWISKO','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP14','G','MIEJSCE PRODUKCJI','WARSZTAT RZEMIEŚLNICZY',NULL,'MIEJSCE PRODUKCJI WARSZTAT RZEMIEŚLNICZY','MIEJ. PROD');
INSERT INTO funkcje VALUES('GP15','G','MIEJSCE PRODUKCJI','INNE',NULL,'MIEJSCE PRODUKCJI INNE','MIEJ. PROD');
INSERT INTO funkcje VALUES('GS01','G','ŚMIETNISKO',NULL,NULL,'ŚMIETNISKO','ŚMIET.');
INSERT INTO funkcje VALUES('GM01','G','ŚMIETNISKO MUSZLOWE',NULL,NULL,'ŚMIETNISKO MUSZLOWE','ŚMIET MUSZ.');
