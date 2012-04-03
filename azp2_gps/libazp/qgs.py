# LIBAZP - klasy AZP2
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

from db import get_postgis_db, get_lite_db
from geom import Feature, geom_str_sql
from qgis.core import QgsCoordinateTransform, QgsCoordinateReferenceSystem, \
    QgsMapLayerRegistry, QgsMapLayer, QgsDataSourceURI, QgsFeature, \
    QgsGeometry

class Layer(object):
    
    layer = None
    added_ids = []
    
    def __init__(self,name,srid=2180):
        reg = QgsMapLayerRegistry.instance()
        self.name = name
        for v in reg.mapLayers().itervalues():
            if v.isValid() and v.type() == QgsMapLayer.VectorLayer and v.name() == name:
                self.layer = v
                break
        self.added_ids = []
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
            return (self.layer.addFeatures([lf]),lf)
        return None
    
    def get_added_ids(self):
        return self.added_ids
    
    def _add_id_signal(self,f):
        self.added_ids.append(f)
        
    def get_info(self):
        dp = self.layer.dataProvider()
        return str(dp.dataSourceUri()+" xx "+str(dp.storageType()))
        
    def edit(self):
        self.layer.startEditing()
        
    def save(self,reload=True):
        if self.layer.commitChanges():
            if reload:
                self.layer.reload()
            return True
        return False

class Layer3D(Layer):
    
    def __init__(self,name,srid=2180):
        Layer.__init__(self,name,srid)
        dp = self.layer.dataProvider()
        self.st = str(dp.storageType()).upper()
        if self.st.startswith('POST'):
            uri = QgsDataSourceURI(dp.dataSourceUri())
            self.db = get_postgis_db(str(uri.database()), str(uri.username()),
                                     str(uri.password()), str(uri.host()), str(uri.port()))
            if name == 'trasy':
                self.ins_fmt = 'insert into trasy values(%(id)s, %(rodzaj)s, %(data)s, %(autor)s, %(dt_pocz)s, %(dt_kon)s,'
                self.ins_fmt += ' %(czest)s, %(uwagi)s, '+geom_str_sql('geom')+")"
        elif self.startswith('SPATIALITE'):
            self.db = get_lite_db('')
        if name == 'trasy':
            self.args_map = {0:'id',1:'rodzaj',2:'data',3:'autor',4:'dt_pocz',5:'dt_kon',6:'czest',7:'uwagi',8:'geom'}
            
    def add_feature(self,f,srid=4326,atr=[]):
        ins_args = self._create_args(atr)
        self.db.update(self.ins_fmt, ins_args, None, False, True)
    
    def _create_args(self,args=[]):
        ins_args = {}
        for (ei,e) in enumerate(args):
            ins_args[self.args_map[ei]] = e
        return ins_args
    
        
    def edit(self):
        pass
    
    def save(self,reload=True):
        self.layer.reload()
        return True

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