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
import re
class Polaczenie(object):
    """ Adapter polaczenia z baza danych PostgreSQL/Postgis albo Sqlite3/Spatialite"""
    PG = 1
    LITE = 2
    SPATIALITE = 3

    def __init__(self, con, typ):
        """ Konstruktor obiektu klasy
        
        con: obiekt Connection zgodny z DBAPI 2.0
        typ: typ bazy do wyboru: 
            - Polaczenie.PG - postgre
            - Polaczenie.LITE - sqlite
        """
        
        self._con = con
        self._tc = typ

    def zatwierdz(self):
        self._con.commit()
        
    def wycofaj(self):
        self._con.rollback()
        
    def zakoncz(self):
        self._con.close()
        self._con = None
    
    def wykonaj(self, sql, vp=[], zatw=True):
        return self.prep(sql).wykonaj(vp,zatw)
        
    def wszystkie(self, sql, vp=[], f=None):
        return self.prep(sql).wszystkie(vp,f)
        
    def jeden(self, sql, vp=[], f=None):
        return self.prep(sql).jeden(vp,f)
    
    _rn = re.compile(':([0-9a-zA-Z_]+)')
    
    def _rep(self,m):
        return '%('+m.group(1)+')s'
        
    def prep(self,sql):
        """ Przygotowuje nowe polecenie do wykonania.
        
        Parametry powinny byc podawane w konwencji uzywanej w module sqlite3. Jezeli
        polaczenie dotyczy bazy Postgresql, to polecenie zostanie przeksztalcone do postaci
        wymaganej przez sterownik psycopg """
        if self._tc in (self.LITE, self.SPATIALITE):
            return Polecenie(self._con,sql)
        ns = self._rn.subn(self._rep,sql.replace('?','%s'))
        return Polecenie(self._con,ns[0])
    
    def getMax(self, tabela, pole='id'):
        sql = 'select coalesce(max(%s), 0) from %s'
        stmt = self.prep(sql%(pole, tabela))
        mx = stmt.jeden()
        return mx[0]

class Polecenie(object):
    """ Polecenie sql przygotowane do wykonania. Ma postac zgodna z 
    wymaganiami sterownika """
    
    def __init__(self, con, prepSql):
        self._ps = prepSql
        self._con = con    
    
    def wykonaj(self, params=[], zatwierdz=True): # mapa albo lista
        """ Wykonanie polecenia DML 
        
        Jezeli zatwierdz == True to zmiany sa natychmiast zatwierdzane"""
        try:
            cur = self._con.cursor()
            cur.execute(self._ps, params)
            cur.close()
            if zatwierdz:
                self._con.commit()
            return cur.rowcount
        except Exception as e:
            print e
            return -1
    
    def wszystkie(self, params=[], f=None):
        """ Wykonanie polecenia SELECT i pobranie wszystkich wierszy z opcjonalna konwersja
        
        f: funkcja konwertujaca kazdy pobrany wiersz """
        cur = self._con.cursor()
        cur.execute(self._ps, params)
        ret = []
        for r in cur.fetchall():
            if f is not None:
                ret.append(f(r))
            else:
                ret.append(r)
        cur.close()
        #print ret
        return ret
    
    def jeden(self, params=[], f=None):
        """ Wykonanie polecenia SELECT i pobranie pierwszeg wiersza z opcjonalna konwersja
        
        f: funkcja konwertujaca kazdy pobrany wiersz """
        cur = self._con.cursor()
        cur.execute(self._ps, params)
        r = cur.fetchone()
        cur.close()
        if r is not None and f is not None:
            return f(r)
        return r
        
def getLite(db, rowFactory=False):
    try:
        import pyspatialite.dbapi2 as lite
        typ = Polaczenie.SPATIALITE
    except ImportError as ie:
        import sqlite3 as lite
        typ = Polaczenie.LITE
    pycon = lite.connect(db)
    if rowFactory:
        pycon.row_factory = lite.Row
    return Polaczenie(pycon, typ)
