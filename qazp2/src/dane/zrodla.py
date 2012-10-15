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
    WNIOSKI_ATR
import sqlite3, psycopg2    
def rejestr_map():
    return QgsMapLayerRegistry.instance()

def get_warstwa(nazwa):
    reg = QgsMapLayerRegistry.instance()
    for v in reg.mapLayers().itervalues():
        if v.isValid() and v.type() == QgsMapLayer.VectorLayer and v.name() == nazwa:
            return v

def _gwarstwa(qgs_warstwa,atrybuty):
    kt = range(len(atrybuty))
    qgs_warstwa.select(kt)
    mt = []
    while True:
        f = QgsFeature()
        if qgs_warstwa.nextFeature(f):
            mt.append(GModel(atrybuty,f))
        else:
            return mt
        
def gstanowiska(qgs_warstwa):
    return _gwarstwa(qgs_warstwa,STANOWISKA_ATR)

def gmiejsca(qgs_warstwa):
    return _gwarstwa(qgs_warstwa, MIEJSCA_ATR)

def gtrasy(qgs_warstwa):
    return _gwarstwa(qgs_warstwa, TRASY_ATR)

_SZUKAJ_IDS = {}

def _szukaj_warstwa(sql,nazwa_warstwy):
    qv = get_warstwa(nazwa_warstwy)
    nuri = QgsDataSourceURI(qv.dataProvider().dataSourceUri())
    nuri.setSql(sql)
    mid = _SZUKAJ_IDS.get(nazwa_warstwy,0)+1
    nwar = QgsVectorLayer(nuri.uri(),nazwa_warstwy+'_szukaj_'+str(mid),qv.dataProvider().name())
    _SZUKAJ_IDS[nazwa_warstwy] = mid
    return nwar

def szukaj_stanowiska(sql):
    return _szukaj_warstwa(sql,'stanowiska')

def szukaj_miejsca(sql):
    return _szukaj_warstwa(sql, 'miejsca')

def szukaj_trasy(sql):
    return _szukaj_warstwa(sql,'trasy')

class Wykaz(object):

    def __init__(self, con, wykNazwa):
        self._con = con
        self._stLista = "select id, nazwa from "+wykNazwa+" where start='%s' order by nazwa"
        self._stLicz = "select count(*) from "+wykNazwa+" where nazwa='%s'"
        self._stMax = "select coalesce(max(id),0) from "+wykNazwa
        self._stZm = "update "+wykNazwa+" set nazwa='%s', start='%s' where id=%d"
        self._stDod = "insert into "+wykNazwa+" values(%d, '%s', '%s')"
        self._stUsu = "delete from "+wykNazwa+" where id=%d"
        self._wykaz = []
        self._start = None
        
    def wypelnij(self, start=None):
        if start is not None:
            self._start = start
        if self._start is None:
            return
        cur = self._con.cursor()
        cur.execute(self._stLista%self._start)
        self._wykaz = []
        for r in cur.fetchall():
            self._wykaz.append((QVariant(r[0]), QVariant(r[1])))
        cur.close()
        return len(self._wykaz)
    
    def dodaj(self,nazwa):
        cur = self._con.cursor()
        un = nazwa.upper()
        cur.execute(self._stLicz%un)
        r = cur.fetchone()[0]
        cur.close()
        if r > 0:
            return False
        cur = self._con.cursor()
        cur.execute(self._stMax)
        n = cur.fetchone()[0]
        cur.close()
        cur = self._con.cursor()
        cur.execute(self._stDod%(n+1,un[:2],un))
        cur.close()
        self._con.commit()
        return True
        
    def usun(self, ident):
        cur = self._con.cursor()
        cur.execute(self._stUsu%ident)
        cur.close()
        self._con.commit()
        
        
    def zmien(self,ident,nazwa):
        un = nazwa.upper()
        cur = self._con.cursor()
        cur.execute(self._stLicz%un)
        r = cur.fetchone()[0]
        cur.close()
        if r > 0:
            return False
        cur = self._con.cursor()
        cur.execute(self._stZm%(un,un[:2],ident))
        cur.close()
        self._con.commit()
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

def getPolaczenie(qgsWarstwa):
    ndp = str(qgsWarstwa.dataProvider().name())
    uri = QgsDataSourceURI(qgsWarstwa.dataProvider().dataSourceUri())
    if ndp.upper() == 'SPATIALITE':
        return sqlite3.connect(str(uri.database()))
        #drv = 'QSQLITE'
    elif ndp.upper == 'POSTGRES':
        #drv = 'QPSQL'
        return psycopg2.connect(database=str(uri.database),host=str(uri.host()),port=int(str(uri.port())),
                                user=str(uri.username()), password=str(uri.password()))
    else:
        raise Exception('Nieobslugiwany typ bazy danych '+ndp)

def _selstmt(atr,tab,ident):
    a = ','.join(atr)
    return 'select '+a+' from '+tab+' where stanowisko='+ident
    
def wyszukajSql(ident, qgsWarstwa, atr, tab):
    p = getPolaczenie(qgsWarstwa)
    cur = p.cursor()
    cur.execute(_selstmt(atr,tab,ident))
    ret = cur.fetchone()
    if ret is None:
        return {'id':-1}
    cur.close()
    p.close()
    dane = {}
    for (ri,r) in enumerate(ret):
        dane[atr[ri]] = r
    return dane

def daneFizg(st,qgsWarstwa):
    return AModel(wyszukajSql(st,qgsWarstwa,JEDFIZG_ATR,'FIZGEO_DANE'))

tabkier = ['N','NE','E','SE','S','SW','W','NW']

def decbin(kier):
    if kier == 0 or kier > 255:
        return ''
    i, n = 0, kier
    bkier = ''
    while n > 1:
        if n % 2 == 1:
            bkier += tabkier[i]+','
        n /= 2
        i+= 1
    return bkier+tabkier[i]

def bindec(kier):
    if len(kier) == 0:
        return 0
    tb = kier.upper().replace(';',',').replace(' ',',').replace(':',',').split(',')
    dkier = 0
    for t in tb:
        if t in tabkier:
            dkier += 2**tabkier.index(t)
        elif t != '':
            return (False,-1)
    return (True,dkier)

def daneEksp(st,qgsWarstwa):
    wys = wyszukajSql(st,qgsWarstwa,EKSPOZYCJA_ATR,'EKSPOZYCJA_DANE')
    wys['stopien'] = wys.get('stopien',0)
    wys['rozmiar'] = wys.get('rozmiar',0)
    wys['kierunek'] = decbin(int(wys.get('kierunek',0)))
    return AModel(wys)

def daneTeren(st,qgsWarstwa):
    return AModel(wyszukajSql(st,qgsWarstwa,TEREN_ATR,'TEREN_DANE'))

def daneObszar(st,qgsWarstwa):
    wys = wyszukajSql(st,qgsWarstwa,OBSZAR_ATR,'OBSZAR_DANE')
    wys['powierzchnia'] = wys.get('powierzchnia',0)
    return AModel(wys)

def daneZagr(st,qgsWarstwa):
    return AModel(wyszukajSql(st,qgsWarstwa,ZAGROZENIA_ATR,'ZAGROZENIA'))

def daneWnio(st,qgsWarstwa):
    return AModel(wyszukajSql(st,qgsWarstwa,WNIOSKI_ATR,'WNIOSKI'))

def _updtstmt(atr,tab,stid):
    a = ','.join(['%s=:%s '%(a,a) for a in atr ])
    return 'update '+tab+' set '+a+' where id = :id and stanowisko='+stid

def _instmt(atr,tab,stid):
    ae = ','.join(atr)
    b = ','.join([':%s'%a for a in atr])
    return 'insert into '+tab+' ('+ae+',stanowisko) values ('+b+','+stid+')'

def _nastid(tab,con):
    cur = con.cursor()
    cur.execute('select coalesce(max(id),0) from '+tab)
    nid = cur.fetchone()[0]+1
    cur.close()
    return nid 

def _genParam(atr,dane):
    return dict([(a,dane.get(a)) for a in atr])

def updtSql(stid, qgsWarstwa, atr, tab,tdane=[]):
    p = getPolaczenie(qgsWarstwa)
    cur = p.cursor()
    us = _updtstmt(atr,tab,stid)
    ins = _instmt(atr,tab,stid)
    uzyty = -1
    for d in tdane:
        pr = _genParam(atr,d)
        pr['id'] = int(pr['id'])
        if pr['id'] > 0:
            cur.execute(us,pr)
            uzyty = 2000+len(tdane)
        else:
            pr['id'] = _nastid(tab,p)
            cur.execute(ins,pr)
            uzyty = 3000+len(tdane)
    p.commit()
    cur.close()
    p.close()
    return uzyty
    
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

def updtObszar(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,OBSZAR_ATR,'OBSZAR_DANE',tdane)

def updtZagr(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,ZAGROZENIA_ATR,'ZAGROZENIA',tdane)

def updtWnio(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,WNIOSKI_ATR,'WNIOSKI',tdane)
