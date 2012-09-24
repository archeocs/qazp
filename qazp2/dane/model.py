'''
Created on Sep 6, 2012

@author: milosz
'''

from qgis.core import QgsFeature, QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform

class AModel(dict):
    
    def __init__(self,dane):
        dict.__init__(self)
        self.zmiany = {}
        for (k,v) in dane.iteritems():
            self[k] = v
            #self.zmiany[k] = False
            
    def __setitem__(self, k,v):
        if not self.zmiany.has_key(k):
            self.zmiany[k] = False
        else:
            self.zmiany[k] = (v != self[k])
        return dict.__setitem__(self, k,v)
    
    def czy_mod(self):
        for k in self.zmiany.iterkeys():
            if self.zmiany[k]:
                return True
        return False
            
    """
    Domyslna implementacja. Kolejnosc kluczy jest niezdefiniowana
    """        
    def kolejnosc(self):
        return self.keys()
    
    """
    Lista wartosci wedlug kolejnosci zwracanej przez funkcje self.kolejnosc
    """
    def lista(self):
        return [self[k] for k in self.kolejnosc()]
    
    def klucz(self,i):
        kt = self.kolejnosc()
        if i < 0 or i >= len(kt):
            raise Exception("klucz: indeks %d poza zakresem [0,%d]"%(i,len(kt)-1))
        return self.kolejnosc()[i]
    
    def zmien(self,mapa):
        for (k,v) in mapa.iteritems():
            self[k] = v
    
    def wartosc(self,i):
        return self[self.klucz(i)]
    
    def submapa(self,*args):
        nm = {}
        for a in args:
            if not self.has_key(a):
                raise Exception("submapa: Nie ma atrybutu "+a)
            nm[a] = self[a]
        return nm
    
    def sublista(self,*args):
        nt = []
        for a in args:
            if not self.has_key(a):
                raise Exception("sublista: nie ma atrybut "+a)
            nt.append(self[a])
        
    
class GModel(AModel):
    
    def __init__(self,kolejnosc,feature):
        AModel.__init__(self,{})
        ma = feature.attributeMap()
        if len(ma) != len(kolejnosc):
            raise Exception("Liczba elementow na liscie %d nie zgadza sie z liczba atrybutow %d"%(len(kolejnosc),len(ma)))
        for (ki, k) in enumerate(kolejnosc):
            self[k] = ma[ki]
        self._kolejnosc = kolejnosc
        self._feature = feature
        
    def kolejnosc(self):
        return self._kolejnosc
    
    def zatwierdz(self):
        self._feature.setAttributeMap(dict([(ki,self[k]) for (ki,k) in enumerate(self.kolejnosc())]))
    
    def feature(self):
        return self._feature
    
    def __unicode__(self):
        return unicode(self)
    
def utworz_feature(atrs,g=None):
    qf = QgsFeature()
    qf.setAttributeMap(dict([(ai,a) for (ai, a) in enumerate(atrs)]))
    if g:
        qf.setGeometry(g)
    return qf

def crs(srid):
    crs = QgsCoordinateReferenceSystem()
    crs.createFromSrid(srid)
    return crs

def zmien_srid(g, osr=4326, dsr=2180):
    if osr != dsr and g.transform(QgsCoordinateTransform(crs(osr),crs(dsr))) != 0:
        raise Exception("Nieudana transformacja")
    return g
