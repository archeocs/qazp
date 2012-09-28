'''
Created on Sep 25, 2012

@author: milosz
'''

from PyQt4.QtCore import QVariant
from dane.zrodla import Warstwa
from qgis.core import QgsFeature
from dane.model import GModel
from qgis.core import QgsCoordinateTransform, QgsCoordinateReferenceSystem


#===============================================================================
# def lista_miejsc(sql):
#    #return []
#    wm = Warstwa("trasy").szukaj(sql)
#    wm.select([0,1,2,3,4,5,7])
#    mt = []
#    f = QgsFeature()
#    ident = 0
#    while True:
#        if wm.nextFeature(f):
#            f.setFeatureId(ident)
#            ident += 1
#            mt.append(GModel(['id','rodzaj_badan','data','autor','rozpoczecie','zakonczenie','uwagi'],f))
#        else:
#            return mt
#===============================================================================

def wybrane(sql):
    return Warstwa("trasy").szukaj(sql)

def pobierz(warstwa):
    warstwa.select([0,1,2,3,4,5,6,7])
    mt = []
    while True:
        f = QgsFeature()
        if warstwa.nextFeature(f):
            mt.append(GModel(['id','rodzaj_badan','data','autor','rozpoczecie','zakonczenie','czestotliwosc','uwagi'],f))
        else:
            return mt
        
def zamien(war,ob):
    f = ob.feature()
    cf = QgsFeature()
    if not war.featureAtId(f.id(),cf):
        raise Exception("Nie ma trasy o podanym id "+f.id())
    war.startEditing()
    for (k, v) in f.attributeMap().iteritems():
        war.changeAttributeValue(f.id(), k,v)
    return (war.commitChanges(),[unicode(a.toString()) for a in cf.attributeMap().itervalues()],f.id(),cf.id())

def dodaj(war,atr,geom,orig_srid=4326):
    f = QgsFeature()
    ni = war.maximumValue(0).toInt()[0]+1 # nowy id
    atr[0] = ni
    f.setAttributeMap(atr)
    wcrs = war.crs()
    ocrs = QgsCoordinateReferenceSystem(orig_srid)
    if ocrs != wcrs:
        if geom.transform(QgsCoordinateTransform(ocrs,wcrs)) != 0:
                raise Exception('Nieudana transformacja')
    f.setGeometry(geom)
    return war.addFeatures([f])

def usun(war,ob):
    f = ob.feature()
    war.startEditing()
    war.deleteFeature(f.id())
    return war.commitChanges()