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

from qgis.core import QgsPoint, QgsPointXY, QgsGeometry

class Punkt(dict):
    """ Klasa reprezentuje punkt okreslony przez dlugosc geograficzna - longitude
    i szerokosc geograficzna - latitiude """
        
    def __init__(self,lon,lat):
        dict.__init__(self)
        self._pt = QgsPoint(float(lon),float(lat))
    
    def punkt(self):
        """ Zwraca punkt w reprezentacji QGI """
        return self._pt
    
    def geom(self):
        """
        Tworzy obiekt geometryczny QgsGeometry uzywany do zapisywania wspolrzednych w QGIS
        """
        return QgsGeometry.fromPointXY(QgsPointXY(self._pt))
  
class Linia(object):
    """ Linia jako lista punktow typu Punkt """      
    
    def __init__(self,punkty=[]):
        self._punkty = []
        self._punkty.extend(punkty)
        
    def dodaj(self,lon,lat):
        """ Dodaje punkt podany jako lon - dlugosc geograficzna i lat - szerokosc """
        np = Punkt(lon,lat)
        self._punkty.append(np)
        return np
    
    def dodaj_linie(self,punkty):
        """ Dodaje linie w postaci listy punktow """
        self._punkty.extend(punkty)
    
    def punkty(self):
        """ Zwraca liste punktow """
        return self._punkty
    
    def polyline(self):
        """ Zwraca linie w reprezentacji QGIS jako liste punktow QGIS """
        return [p.punkt() for p in self._punkty]
    
    def geom(self):
        """ Tworzy obiekt gemetryczny QGIS QgsGeometry reprezentujacy linie"""
        return QgsGeometry.fromPolyline(self.polyline())