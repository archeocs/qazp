'''
Created on Mar 23, 2012

@author: milosz
'''

from qgis.core import QgsMapLayerRegistry, QgsMapLayer, QgsDataSourceURI, QgsFeature,QgsGeometry
from qgis.core import  QgsCoordinateTransform, QgsCoordinateReferenceSystem
from geom import Feature

class Layer(object):
    
    layer = None
    
    def __init__(self,name,srid=2180):
        reg = QgsMapLayerRegistry.instance()
        for v in reg.mapLayers().itervalues():
            if v.isValid() and v.type() == QgsMapLayer.VectorLayer and v.name() == name:
                self.layer = v
                break
        self.crs = QgsCoordinateReferenceSystem()
        self.crs.createFromSrid(srid)
    
    def max_id(self):
        mv = self.layer.maximumValue(0)
        return mv.toInt()[0]
    
    def add_feature(self,f,srid=4326,atr=[]):
        if isinstance(f, Feature):
            geom = QgsGeometry.fromWkt(f.wkt())
            origcrs = QgsCoordinateReferenceSystem()
            origcrs.createFromSrid(srid)
            if geom.transform(QgsCoordinateTransform(origcrs,self.crs)) != 0:
                raise Exception('Nieudana transformacja')
            map_atr = {}
            for (ai,a) in enumerate(atr):
                map_atr[ai] = a
            lf = QgsFeature()
            lf.setGeometry(geom)
            lf.setAttributeMap(map_atr)
            return self.layer.addFeature(lf)
        
    def edit(self):
        self.layer.startEditing()
        
    def save(self,reload=True):
        if self.layer.commitChanges():
            if reload:
                self.layer.reload()
            return True
        return False


class Settings(object):
    
    def __init__(self,qs):
        self.qs = qs
        
    def get_value(self,group,name):
        self.qs.beginGroup(group)
        if self.qs.contains(name):
            v = self.qs.value(name)
        else:
            v = None # brak wartosci o podanej nazwie
        self.qs.endGroup()
        return v
    
    def get_lite_path(self):
        condb = self.get_value('/SpatiaLite', 'connections/selected')
        if condb:
            namedb = condb.toString().split('@')[0]
        else:
            return "Brak I" # brak wybranej bazy
        pathdb = self.get_value('/SpatiaLite/connections/'+namedb,'sqlitepath')
        if pathdb:
            return pathdb.toString()
        return "Brak II "+namedb
    
    def get_pg_dict(self):
        condb = self.get_value('/PostgreSQL', 'connections/selected')
        if condb:
            namedb = condb.toString()
        else:
            return None # brak wybranej bazy
        pg = {}
        pg['host'] = self.get_value('/PostgreSQL/connections/'+namedb,'host').toString()
        pg['port'] = self.get_value('/PostgreSQL/connections/'+namedb,'port').toString()
        pg['db'] = self.get_value('/PostgreSQL/connections/'+namedb,'database').toString()
        pg['user'] = self.get_value('/PostgreSQL/connections/'+namedb,'username').toString()
        pg['pswd'] = self.get_value('/PostgreSQL/connections/'+namedb,'password').toString()
        return pg
    
def lite_uri(path,table,geom_col,pk):
    uri = QgsDataSourceURI()
    uri.setDatabase(path)
    uri.setDataSource('',aTable=table,aGeometryColumn=geom_col,aKeyColumn=pk)
    return uri

def pg_uri(pg_dict):
    uri = QgsDataSourceURI()
    uri.setConnection(pg_dict['host'], pg_dict['port'], pg_dict['db'], pg_dict['user'], pg_dict['pswd'])
    return uri