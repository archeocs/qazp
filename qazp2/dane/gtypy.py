'''
Created on Sep 8, 2012

@author: milosz
'''

from qgis.core import QgsPoint,QgsGeometry

class Punkt(dict):
    
    def __init__(self,lon,lat):
        dict.__init__(self)
        self._pt = QgsPoint(float(lon),float(lat))
    
    def punkt(self):
        return self._pt
    
    def geom(self):
        return QgsGeometry.fromPoint(self._pt)
    
class Linia(object):
    
    def __init__(self,punkty=[]):
        self._punkty = []
        self._punkty.extend(punkty)
        
    
    def dodaj(self,lon,lat):
        np = Punkt(lon,lat)
        self._punkty.append(np)
        return np
    
    def dodaj_linie(self,punkty):
        self._punkty.extend(punkty)
    
    def punkty(self):
        return self._punkty
    
    def polyline(self):
        return [p.punkt() for p in self._punkty]
    
    def geom(self):
        return QgsGeometry.fromPolyline(self.polyline())