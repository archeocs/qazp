# -*- coding: utf-8 -*-

# (c) Milosz Piglas 2012 Wszystkie prawa zastrzezone

#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
# 
#      * Redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above
#  copyright notice, this list of conditions and the following disclaimer
#  in the documentation and/or other materials provided with the
#  distribution.
#      * Neither the name of Milosz Piglas nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
# 
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


def getUstawienia(con, klucz, domyslna=None):
    stmt = con.prep('select wartosc from ustawienia where klucz = ?')
    w = stmt.jeden([klucz.upper()])
    if w is None:
        return domyslna
    return w[0]

def setUstawienia(con, klucz, wartosc):
    stdKlucz = klucz.upper()
    sw = getUstawienia(con, stdKlucz)
    if sw is None:
        stmt = con.prep('insert into ustawienia values(:klucz,:wartosc)')
    elif sw < wartosc:
        stmt = con.prep('update ustawienia set wartosc=:wartosc where klucz=:klucz')
    if stmt.wykonaj({'klucz':stdKlucz, 'wartosc':wartosc},False) != 1:
        con.wycofaj()
        return False
    else:
        con.zatwierdz()
        return True

def sprSchemat(con,oczekiwany):
    ws = getUstawienia(con, 'wersja', '0000')
    return (ws >= oczekiwany, ws)

def getSchemat(con):
    return getUstawienia(con, 'wersja', '0000')

def dodajMedia(con):
    crTab = "create table media(id integer not null primary key, sygnatura varchar(50),"\
            " plik varchar(20), format varchar(4), tabela varchar(1), dane blob)"    
    con.prep(crTab).wykonaj(zatwierdz=False)
    crTab = "CREATE TABLE st_media(medium integer, stanowisko integer, typ varchar(1))"    
    con.prep(crTab).wykonaj(zatwierdz=False)
    con.prep('drop trigger del_stanowisko').wykonaj(zatwierdz=False)
    crTrig = """CREATE TRIGGER del_stanowisko before delete on stanowiska 
                begin
                    delete from ekspozycja_dane where stanowisko = OLD.id;
                    delete from fizgeo_dane where stanowisko = OLD.id;
                    delete from teren_dane where stanowisko = OLD.id;
                    delete from wnioski where stanowisko = OLD.id;
                    delete from zagrozenia where stanowisko = OLD.id;
                    delete from fakty where stanowisko = OLD.id;
                    delete from karty where stanowisko = OLD.id;
                    delete from obszar_dane where stanowisko = OLD.id;
                    delete from aktualnosci where stanowisko = OLD.id;
                    delete from media where id = (select medium from st_media where stanowisko = OLD.id);
                    delete from st_media where stanowisko = OLD.id;
                end;
            """
    con.prep(crTrig).wykonaj(zatwierdz=False)
    
def dodajKolumnePochodzenie0002(con):
    altKarty = "alter table karty add column pochodzenie_danych integer"
    con.prep(altKarty).wykonaj(zatwierdz=False)

def utworzWykaz(con, nazwa):
    createSql = "CREATE TABLE %s " \
                "(" \
                "ID INTEGER PRIMARY KEY," \
                "START VARCHAR(2)," \
                "NAZWA VARCHAR(255)" \
                ")"
    con.prep(createSql % nazwa).wykonaj(zatwierdz=False)

def utworzZdjeciaLotnicze(con):
    createZdjecia = "CREATE TABLE ZDJECIA_LOTNICZE(" \
                    "ID INTEGER NOT NULL," \
                    "FOLDER VARCHAR(20)," \
                    "KLATKA VARCHAR(20)," \
                    "MIEJSCOWOSC INTEGER," \
                    "GMINA INTEGER," \
                    "POWIAT INTEGER," \
                    "WOJEWODZTWO INTEGER," \
                    "AUTOR INTEGER," \
                    "PILOT INTEGER," \
                    "DATA_WYKONANIA VARCHAR(10)," \
                    "CZAS_WYKONANIA VARCHAR(20)," \
                    "PRAWA_AUTORSKIE VARCHAR(255)," \
                    "PROJEKT INTEGER," \
                    "NUMER VARCHAR(100)," \
                    "ZLECENIODAWCA INTEGER," \
                    "PLATNIK INTEGER," \
                    "NOSNIK VARCHAR(1)," \
                    "CONSTRAINT PK_ZDJECIA_LOTNICZE PRIMARY KEY (ID)," \
                    "CONSTRAINT UNIQUE_ZDJECIA_LOTNICZE UNIQUE (FOLDER, KLATKA)" \
                    ")"
    con.prep(createZdjecia).wykonaj(zatwierdz=False)
    con.prep("SELECT ADDGEOMETRYCOLUMN('ZDJECIA_LOTNICZE', 'WSPOLRZEDNE',2180, 'POINT', 'XY')").wykonaj(zatwierdz=False)


def wykonajPolecenie(con, stmt, zatwierdz=False):
    return con.prep(stmt).wykonaj(zatwierdz=zatwierdz)

_BIEZ_SCHEMAT = '0003' # ostatnia wersja schematu bazy

def dostosujSchemat(con):
    ss = sprSchemat(con, _BIEZ_SCHEMAT)
    if ss[0]:
        return True
    schBaza = ss[1]
    if schBaza == '0000':
        dodajMedia(con)
        if setUstawienia(con, 'wersja', '0001'):
            schBaza = '0001'
    if schBaza == '0001':
        dodajKolumnePochodzenie0002(con)
        if setUstawienia(con, 'wersja', '0002'):
            schBaza = '0002'
    if schBaza == '0002':
        if con._tc == 3:
            utworzWykaz(con, 'PODMIOTY')
            utworzWykaz(con, 'PROJEKTY')
            utworzZdjeciaLotnicze(con)
        else:
            return False
        if setUstawienia(con, 'wersja', '0003'):
            schBaza = '0003'
    # if schBaza == '0002'
    # ...
    return schBaza == _BIEZ_SCHEMAT
