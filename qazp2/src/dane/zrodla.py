'''
Created on Sep 7, 2012

@author: milosz
'''

from qgis.core import QgsMapLayerRegistry, QgsMapLayer,QgsFeature
from qgis.core import QgsVectorLayer, QgsDataSourceURI
from dane.model import MIEJSCA_ATR,GModel, TRASY_ATR,STANOWISKA_ATR, AModel,\
    JEDFIZG_ATR,  EKSPOZYCJA_ATR, TEREN_ATR, OBSZAR_ATR, ZAGROZENIA_ATR,\
    WNIOSKI_ATR
import sqlite3, psycopg2    
import logging
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
    logging.info('wyszukaj '+str(ret))
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

def daneEksp(st,qgsWarstwa):
    wys = wyszukajSql(st,qgsWarstwa,EKSPOZYCJA_ATR,'EKSPOZYCJA_DANE')
    if not wys.has_key('stopien'):
        wys['stopien'] = 0
    if not wys.has_key('rozmiar'):
        wys['rozmiar'] = 0
    return AModel(wys)

def daneTeren(st,qgsWarstwa):
    return AModel(wyszukajSql(st,qgsWarstwa,TEREN_ATR,'TEREN_DANE'))

def daneObszar(st,qgsWarstwa):
    wys = wyszukajSql(st,qgsWarstwa,OBSZAR_ATR,'OBSZAR_DANE')
    if not wys.has_key('powierzchnia'):
        wys['powierzchnia'] = 0
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
    logging.info(us)
    logging.info(ins)
    for d in tdane:
        pr = _genParam(atr,d)
        logging.info('pr '+str(pr))
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
    return updtSql(st,qgsWarstwa,EKSPOZYCJA_ATR,'EKSPOZYCJA_DANE',tdane)

def updtTeren(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,TEREN_ATR,'TEREN_DANE',tdane)

def updtObszar(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,OBSZAR_ATR,'OBSZAR_DANE',tdane)

def updtZagr(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,ZAGROZENIA_ATR,'ZAGROZENIA',tdane)

def updtWnio(st,qgsWarstwa,tdane=[]):
    return updtSql(st,qgsWarstwa,WNIOSKI_ATR,'WNIOSKI',tdane)