'''
Created on Sep 7, 2012

@author: milosz
'''

from qgis.core import QgsMapLayerRegistry, QgsMapLayer,QgsFeature
from qgis.core import QgsVectorLayer, QgsDataSourceURI
from dane.model import MIEJSCA_ATR,GModel, TRASY_ATR
    
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

def szukaj_miejsca(sql):
    return _szukaj_warstwa(sql, 'miejsca')

def szukaj_trasy(sql):
    return _szukaj_warstwa(sql,'trasy')