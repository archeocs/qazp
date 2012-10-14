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
from qgis.core import QgsFeature
from dane.model import MIEJSCA_ATR
from qgis.core import QgsCoordinateTransform, QgsCoordinateReferenceSystem


def set_atr(qgs_obiekt,atr,v):
    if atr not in MIEJSCA_ATR:
        return False
    ai = MIEJSCA_ATR.index(atr)
    qgs_obiekt.changeAttribute(ai,QVariant(v))
    return True

def setAtr(qgsObiekt, atr, v, lista):
    if atr not in lista:
        return False
    ai = lista.index(atr)
    qgsObiekt.changeAttribute(ai,QVariant(v))
    return True

def setMapa(qgsObiekt,mapa,lista):
    for (k,v) in mapa.iteritems():
        setAtr(qgsObiekt,k,v,lista)

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

