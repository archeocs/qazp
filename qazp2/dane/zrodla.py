'''
Created on Sep 7, 2012

@author: milosz
'''

from qgis.core import QgsMapLayerRegistry, QgsMapLayer
from qgis.core import QgsVectorLayer, QgsDataSourceURI

class Warstwa(object):
    
    def __init__(self,nazwa):
        reg = QgsMapLayerRegistry.instance()
        self._nazwa = nazwa
        self.szuk_id = 0
        for v in reg.mapLayers().itervalues():
            if v.isValid() and v.type() == QgsMapLayer.VectorLayer and v.name() == nazwa:
                self._war = v
                break
            
    def szukaj(self,sql):
        nuri = QgsDataSourceURI(self._war.dataProvider().dataSourceUri())
        nuri.setSql(sql)
        #ndp = QgsVectorDataProvider(self._war.dataProvider().dataSourceUri())
        #ndp.setSubsetString(sql)
        nwar = QgsVectorLayer(nuri.uri(),"szukaj "+str(self.szuk_id+1),self._war.dataProvider().name())
        self.szuk_id += 1
        return nwar
    
    def max_id(self):
        return self._war.maximumValue(0)
    
def rejestr_map():
    return QgsMapLayerRegistry.instance()

def get_warstwa(nazwa):
    reg = QgsMapLayerRegistry.instance()
    for v in reg.mapLayers().itervalues():
        if v.isValid() and v.type() == QgsMapLayer.VectorLayer and v.name() == nazwa:
            return v

class Wfs(object):
    
    def __init__(self,uri):
        self._war = QgsVectorLayer(uri,"wfs")