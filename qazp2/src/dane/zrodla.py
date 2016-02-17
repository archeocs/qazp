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

from PyQt4.QtCore import QVariant
from qgis.core import QgsMapLayerRegistry, QgsMapLayer,QgsFeature
from qgis.core import QgsVectorLayer, QgsDataSourceURI
from dane.model import MIEJSCA_ATR,GModel, TRASY_ATR,STANOWISKA_ATR, AModel,\
    JEDFIZG_ATR,  EKSPOZYCJA_ATR, TEREN_ATR, OBSZAR_ATR, ZAGROZENIA_ATR,\
    WNIOSKI_ATR, GLEBA_ATR, AKTUALNOSCI_ATR, KARTA_ATR, ZDJECIA_LOTNICZE_ATR, NowyModel
from micon import Polaczenie, getLite
import logging
def rejestr_map():
    """ Zwraca rejestr map z QGIS """
    return QgsMapLayerRegistry.instance()

def get_warstwa(nazwa):
    """ Wyszukuje warstwe wedlug nazwy i zwraca pierwsza znaleziona """
    nup = nazwa.upper()
    reg = QgsMapLayerRegistry.instance()
    for v in reg.mapLayers().itervalues():
        if v.isValid() and v.type() == QgsMapLayer.VectorLayer and unicode(v.name()).upper() == nup:
            return v

def _gwarstwa(qgs_warstwa,atrybuty):
    """ Dla podanej warstwy pobiera informacje o wszystkich obiektach geometrycznych 
        i dla kazdego z nich tworzy nowa instancje klasy model.GModel """
    kt = range(len(atrybuty))
    qgs_warstwa.select(kt)
    mt = []
    while True:
        f = QgsFeature()
        if qgs_warstwa.nextFeature(f):
            mt.append(GModel(atrybuty,f))
        else:
            return mt

def _obiekty(qgsWarstwa, atrybuty):
    qgsWarstwa.selectAll()
    mt = []
    for f in qgsWarstwa.selectedFeatures():
        mt.append(NowyModel(atrybuty, f))
    return mt

def sqlListaId(con, sql, params=[]):
    stmt = con.prep(sql)
    return set(stmt.wszystkie(params, f=lambda r : r[0]))    

def _listaMap(listaObi, atrybuty):
    return [GModel(atrybuty,f) for f in listaObi]

def _konwertuj(listaObi, atrybuty):
    return [NowyModel(atrybuty, f) for f in listaObi]

def zdjeciaLista(listaObi):
    return _konwertuj(listaObi, ZDJECIA_LOTNICZE_ATR)

def stLista(listaObi):
    return _konwertuj(listaObi, STANOWISKA_ATR)
        
def gstanowiska(qgs_warstwa):
    return _obiekty(qgs_warstwa,STANOWISKA_ATR)

def gzdjecia(qgsWarstwa):
    return _obiekty(qgsWarstwa, ZDJECIA_LOTNICZE_ATR)

def gmiejsca(qgs_warstwa):
    return _obiekty(qgs_warstwa, MIEJSCA_ATR)

def gtrasy(qgs_warstwa):
    return _obiekty(qgs_warstwa, TRASY_ATR)

_SZUKAJ_IDS = {}

def _szukaj_warstwa(sql,nazwa_warstwy):
    """ Wyszukuje na warstwie wszystkie obiekty, ktore spelniaja polecenie sql i zwraca je w postaci
        nowej warstwy QgsVectorLayer"""
    qv = get_warstwa(nazwa_warstwy)
    nuri = QgsDataSourceURI(qv.dataProvider().dataSourceUri())
    nuri.setSql(sql)
    mid = _SZUKAJ_IDS.get(nazwa_warstwy,0)+1
    nwar = QgsVectorLayer(nuri.uri(),nazwa_warstwy+'_szukaj_'+str(mid),qv.dataProvider().name())
    _SZUKAJ_IDS[nazwa_warstwy] = mid
    return nwar

def szukaj_zdjecia(sql):
    return _szukaj_warstwa(sql, 'zdjecia_lotnicze')

def szukaj_stanowiska(sql):
    return _szukaj_warstwa(sql,'stanowiska')

def szukaj_miejsca(sql):
    return _szukaj_warstwa(sql, 'miejsca')

def szukaj_trasy(sql):
    return _szukaj_warstwa(sql,'trasy')

class Wykaz(object):

    def __init__(self, con, wykNazwa):
        self._con = con
        self._stLista = self._con.prep("select id, nazwa from "+wykNazwa+" where start=? order by nazwa")
        self._stLicz = self._con.prep("select count(*) from "+wykNazwa+" where nazwa=?")
        self._stMax = self._con.prep("select coalesce(max(id),0) from "+wykNazwa)
        self._stZm = self._con.prep("update "+wykNazwa+" set nazwa=?, start=? where id=?")
        self._stDod = self._con.prep("insert into "+wykNazwa+" values(?, ?, ?)")
        self._stUsu = self._con.prep("delete from "+wykNazwa+" where id=?")
        self._wykaz = []
        self._start = None
        
    def wypelnij(self, start=None):
        if start is not None:
            self._start = start
        if self._start is None:
            return
        self._wykaz = []
        for r in self._stLista.wszystkie([self._start]):
            self._wykaz.append((r[0],r[1]))
        return len(self._wykaz)
    
    def dodaj(self,nazwa):
        un = nazwa.upper()
        r = self._stLicz.jeden([un])[0]
        if r > 0:
            return False
        n = self._stMax.jeden()[0]
        self._stDod.wykonaj([n+1,un[:2],un])
        return True
        
    def usun(self, ident):
        self._stUsu.wykonaj([ident])
        
    def zmien(self,ident,nazwa):
        un = nazwa.upper()
        r = self._stLicz.jeden([un])[0]
        if r > 0:
            return False
        self._stZm.wykonaj([un,un[:2],ident])
        return True
    
    def __len__(self):
        return len(self._wykaz)
    
    def __getitem__(self, ind):
        return self.nazwa(ind)
        
    def nazwa(self, ind, pystr=False):
        if 0 <= ind < len(self._wykaz):
            if pystr:
                return unicode(self._wykaz[ind].toString())
            return self._wykaz[ind]
        raise Exception('indeks %d poza zakresem %d'%(ind,len(self._wykaz)))

def getPolaczenie2(qgsWarstwa, wierszMapa = False):
    ndp = str(qgsWarstwa.dataProvider().name())
    uri = QgsDataSourceURI(qgsWarstwa.dataProvider().dataSourceUri())
    if ndp.upper() == 'SPATIALITE':
        #import sqlite3
        #con = sqlite3.connect(str(uri.database()))
        con = getLite(str(uri.database()), wierszMapa)
        return con
        #if wierszMapa:
        #    con.row_factory = sqlite3.Row
        #return Polaczenie(con, Polaczenie.LITE)
    elif ndp.upper() == 'POSTGRES':
        import psycopg2
        import psycopg2.extensions
        import psycopg2.extras
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
        rowFactory = None
        if wierszMapa:
            rowFactory = psycopg2.extras.DictCursor
        return Polaczenie(psycopg2.connect(database=str(uri.database()),host=str(uri.host()),port=str(uri.port()),
                                user=str(uri.username()), password=str(uri.password()), cursor_factory = rowFactory),Polaczenie.PG)
    else:
        raise Exception('Nieobslugiwany typ bazy danych '+ndp)

def _selstmt(atr,tab):
    a = ','.join(atr)
    return 'select '+a+' from '+tab+' where stanowisko=? order by id asc'

def _filtruj(wiersze):
    if wiersze is None or len(wiersze) == 0:
        return None
    else:
        return wiersze[0]
    
def wyszukajSql(ident, qgsWarstwa, atr, tab):
    p = getPolaczenie2(qgsWarstwa)
    ret = _filtruj(p.wszystkie(_selstmt(atr,tab),[ident]))
    if ret is None:
        return {'id':-1}
    p.zakoncz()
    dane = {}
    for (ri,r) in enumerate(ret):
        dane[atr[ri]] = r
    return dane

def daneFizg(st,qgsWarstwa):
    return AModel(wyszukajSql(st,qgsWarstwa,JEDFIZG_ATR,'FIZGEO_DANE'))

tabkier = ['N','NE','E','SE','S','SW','W','NW']
tabpochodzenie = ['A','T','X','N','W','P','L']

def decbin(kier, wartosci=tabkier):
    if kier == 0 or kier > 255:
        return ''
    i, n = 0, kier
    bkier = ''
    while n > 1:
        if n % 2 == 1:
            bkier += wartosci[i]+','
        n /= 2
        i+= 1
    return bkier+wartosci[i]

def bindec(kier, wartosci=tabkier):
    if len(kier) == 0:
        return (True,0)
    tb = kier.upper().replace(';',',').replace(' ',',').replace(':',',').split(',')
    dkier = 0
    for t in tb:
        if t in wartosci:
            dkier += 2**wartosci.index(t)
        elif t != '':
            return (False,-1)
    return (True,dkier)

def daneEksp(st,qgsWarstwa):
    wys = wyszukajSql(st,qgsWarstwa,EKSPOZYCJA_ATR,'EKSPOZYCJA_DANE')
    wys['stopien'] = wys.get('stopien',0)
    wys['rozmiar'] = wys.get('rozmiar',0)
    kier = wys.get('kierunek',0)
    if kier is None:
        kier = 0
    wys['kierunek'] = decbin(int(kier))
    return AModel(wys)

def daneTeren(st,qgsWarstwa):
    return AModel(wyszukajSql(st,qgsWarstwa,TEREN_ATR,'TEREN_DANE'))

def daneGleba(st,qgsWarstwa):
    return AModel(wyszukajSql(st,qgsWarstwa,GLEBA_ATR,'GLEBA_DANE'))

def daneObszar(st,qgsWarstwa):
    wys = wyszukajSql(st,qgsWarstwa,OBSZAR_ATR,'OBSZAR_DANE')
    ps = wys.get('powierzchnia', 0)
    if ps is not None:
        wys['powierzchnia'] = float(str(ps).replace(',','.'))
    else:
        wys['powierzchnia'] = 0.0
    return AModel(wys)

def daneZagr(st,qgsWarstwa):
    return AModel(wyszukajSql(st,qgsWarstwa,ZAGROZENIA_ATR,'ZAGROZENIA'))

def daneWnio(st,qgsWarstwa):
    return AModel(wyszukajSql(st,qgsWarstwa,WNIOSKI_ATR,'WNIOSKI'))

def daneAkt(st,qgsWarstwa):
    return AModel(wyszukajSql(st,qgsWarstwa,AKTUALNOSCI_ATR,'AKTUALNOSCI'))

def daneKarta(st,qgsWarstwa):
    wys = wyszukajSql(st,qgsWarstwa,KARTA_ATR,'KARTY')
    pochodzenie = wys.get('pochodzenie_danych', 0)
    if pochodzenie is None:
        pochodzenie = 0
    wys['pochodzenie_danych'] = decbin(int(pochodzenie), tabpochodzenie)
    return AModel(wys)

def _updtstmt2(atr, tab, stid):
    a = ','.join(['%s=:%s'%(a,a) for a in atr])
    return 'update '+tab+' set '+a+' where id = :id and stanowisko='+stid

def _insstmt2(atr, tab, stid):
    ae = ','.join(atr)
    b = ','.join([':%s'%a for a in atr])
    return 'insert into '+tab+' ('+ae+',stanowisko) values ('+b+','+stid+')'

def _genParam(atr,dane):
    return dict([(a,dane.get(a)) for a in atr])

def updtSql(stid, qgsWarstwa, atr, tab,tdane=[]):
    p = getPolaczenie2(qgsWarstwa)
    us = p.prep(_updtstmt2(atr[1:],tab,stid)) # a[1:] aby pominac parametr 'id'
    ins = p.prep(_insstmt2(atr,tab,stid))
    uzyty = -1
    nowyId = None
    for d in tdane:
        pr = _genParam(atr,d)
        pr['id'] = int(pr['id'])
        if pr['id'] > 0:
            logging.info("ZMIENIAM %s wartosci: %s"%(tab,str(pr)))
            us.wykonaj(pr, False)
            uzyty = 2000+len(tdane)
        else:
            pr['id'] = p.jeden('select coalesce(max(id),0) from '+tab)[0]+1
            logging.info("DODAJE %s wartosci: %s"%(tab,str(pr)))
            ins.wykonaj(pr, False)
            uzyty = 3000+len(tdane)
            nowyId = pr['id']
    p.zatwierdz()
    p.zakoncz()
    return nowyId
    
def updtFizg(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,JEDFIZG_ATR,'FIZGEO_DANE',tdane)

def updtEkspo(st,qgsWarstwa,tdane=[]):
    td = []
    td.extend(tdane)
    for d in td:
        dk = bindec(d.get('kierunek',''))
        if dk[0]:
            d['kierunek'] = dk[1]
        else:
            raise Exception(u'Nieprawidlowe okreslenie kierunku '+d.get('kierunek',''))
    return updtSql(st,qgsWarstwa,EKSPOZYCJA_ATR,'EKSPOZYCJA_DANE',td)

def updtTeren(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,TEREN_ATR,'TEREN_DANE',tdane)

def updtGleba(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,GLEBA_ATR,'GLEBA_DANE',tdane)

def updtObszar(st,qgsWarstwa,tdane=[]):
    td = []
    td.extend(tdane)
    for d in td:
        if d['powierzchnia'] != None:
            d['powierzchnia'] = float(str(d['powierzchnia']).replace(',','.'))
    return updtSql(st,qgsWarstwa,OBSZAR_ATR,'OBSZAR_DANE',td)

def updtZagr(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,ZAGROZENIA_ATR,'ZAGROZENIA',tdane)

def updtWnio(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,WNIOSKI_ATR,'WNIOSKI',tdane)

def updtAkt(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,AKTUALNOSCI_ATR,'AKTUALNOSCI',tdane)

def updtKarta(st,qgsWarstwa,tdane=[]):
    td = []
    td.extend(tdane)
    for d in td:
        dp = bindec(d.get('pochodzenie_danych', ''), tabpochodzenie)
        if dp[0]:
            d['pochodzenie_danych'] = dp[1]
        else:
            raise Exception(u'Nieprawidlowe okreslenie pochodzenia danych '+d.get('pochodzenie_danych',''))
    return updtSql(st,qgsWarstwa,KARTA_ATR,'KARTY',td)

