'''
Created on Sep 29, 2012

@author: milosz
'''
from PyQt4.QtCore import QVariant
from qgis.core import QgsFeature
from dane.model import MIEJSCA_ATR
from qgis.core import QgsCoordinateTransform, QgsCoordinateReferenceSystem


def set_atr(qgs_obiekt,atr,v):
    if atr not in MIEJSCA_ATR:
        return False
    ai = MIEJSCA_ATR.index(atr)
    qgs_obiekt.changeAttribute(ai,QVariant(v))
    return True

def set_mapa(qgs_obiekt,mapa):
    for (k,v) in mapa.iteritems():
        set_atr(qgs_obiekt,k,v)
    
def zmien(qgs_warstwa,qgs_obiekt):
    am = qgs_obiekt.attributeMap()
    fid = qgs_obiekt.id()
    qgs_warstwa.startEditing()
    for (k,v) in am.iteritems():
        qgs_warstwa.changeAttributeValue(fid, k,v)
    return qgs_warstwa.commitChanges()

def usun(qgs_warstwa,qgs_obiekt):
    qgs_warstwa.startEditing()
    qgs_warstwa.deleteFeature(qgs_obiekt.id())
    return qgs_warstwa.commitChanges()

def dodaj(qgs_warstwa,atr,qgs_geom,orig_srid=4326,commit=False):
    f = QgsFeature()
    ni = qgs_warstwa.maximumValue(0).toInt()[0]+1 # nowy id
    atr[0] = ni
    f.setAttributeMap(atr)
    wcrs = qgs_warstwa.crs()
    ocrs = QgsCoordinateReferenceSystem(orig_srid)
    if ocrs != wcrs:
        if qgs_geom.transform(QgsCoordinateTransform(ocrs,wcrs)) != 0:
                raise Exception('Nieudana transformacja')
    f.setGeometry(qgs_geom)
    if commit:
        qgs_warstwa.startEditing()
    return qgs_warstwa.addFeatures([f]) and (not commit or qgs_warstwa.commitChanges())

