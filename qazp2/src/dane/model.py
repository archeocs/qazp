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

from qgis.core import QgsFeature, QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform
from PyQt4.QtCore import QVariant
class AModel(dict):
    """
    Prosty model dany, w ktorym rozszerzone sa funkcjonalnosci zwyklego
    slownika
    """
    def __init__(self,dane,domyslne={}):
        dict.__init__(self)
        self.zmiany = {}
        self._dom = domyslne
        for (k,v) in dane.iteritems():
            if v is None:
                self[k] = QVariant(domyslne.get(k))
            else:
                self[k] = QVariant(v)
            
    def __setitem__(self, k,v):
        """ Wstawia wartosc do slownika i zapamietuje klucz, jezeli jego wartosc
            jest zmieniana"""
        if not self.zmiany.has_key(k):
            self.zmiany[k] = False
        else:
            self.zmiany[k] = (v != self[k])
        return dict.__setitem__(self, k,v)
    
    def czy_mod(self):
        """ Sprawdza, czy dane w slowniku byly modyfikowane """
        for k in self.zmiany.iterkeys():
            if self.zmiany[k]:
                return True
        return False
               
    def kolejnosc(self):
        """  Domyslna implementacja. Kolejnosc kluczy jest niezdefiniowana    """     
        return self.keys()
    
    def lista(self):
        """Lista wartosci wedlug kolejnosci zwracanej przez funkcje self.kolejnosc """
        return [self[k] for k in self.kolejnosc()]
    
    def klucz(self,i):
        """ zwraca i-ty klucz wedlug podanej kolejnosci. 
        
        W domyslnej implemntacji kolejnosc kluczy jest przypadkowa. Zeby to zmienic trzeba
        nadpisac metode AModel.kolejnosc()"""
        kt = self.kolejnosc()
        if i < 0 or i >= len(kt):
            raise Exception("klucz: indeks %d poza zakresem [0,%d]"%(i,len(kt)-1))
        return self.kolejnosc()[i]
    
    def zmien(self,mapa):
        """ Zmienia dane w slowniku wedlug zawartosci innej mapy przekazanej w parametrze metody """
        for (k,v) in mapa.iteritems():
            self[k] = v
    
    def wartosc(self,i):
        """ Zwraca i-ta wartosc ze slownika
        
        W domyslnej implemntacji kolejnosc kluczy jest przypadkowa. Zeby to zmienic trzeba
        nadpisac metode AModel.kolejnosc() """
        return self[self.klucz(i)]
    
    def submapa(self,*args):
        """ Zwraca podzbior kluczy i wartosci wedlug podanej listy kluczy """
        nm = {}
        for a in args:
            if not self.has_key(a):
                raise Exception("submapa: Nie ma atrybutu "+a)
            nm[a] = self[a]
        return nm
    
    def sublista(self,*args):
        """ Zwraca podzbior wartosci wedlug podanej listy kluczy """
        nt = []
        for a in args:
            if not self.has_key(a):
                raise Exception("sublista: nie ma atrybut "+a)
            nt.append(self[a])
        
    
class GModel(AModel):
    """ Model danych do obslugi informacji pochodzacych z QGIS"""
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
        """ Wprowadza wlasciwosci obiektu geometrycznego na podstawie zawartosci slownika """
        self._feature.setAttributeMap(dict([(ki,self[k]) for (ki,k) in enumerate(self.kolejnosc())]))
        
    def aktualizuj(self):
        ma = self._feature.attributeMap()
        for (ki, k) in enumerate(self._kolejnosc):
            self[k] = ma[ki]
    
    def feature(self):
        """ Zwraca obiekt geometryczny """
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

MIEJSCA_ATR = ['id','nazwa','rodzaj_badan','data','autor','uwagi']

TRASY_ATR = ['id','rozpoczecie','zakonczenie','czestotliwosc','rodzaj_badan','data','autor','uwagi']

STANOWISKA_ATR = ['id','obszar','nr_obszar','miejscowosc','nr_miejscowosc','gmina','powiat','wojewodztwo',
                  'rodzaj_badan','data','autor','uwagi']

JEDFIZG_ATR = ['id','nadmorska','w_morzu','plaza','mierzeja','skarpa','wal_wydmowy','duze_doliny',
            'w_wodzie','ter_denna','ter_nadzalewowa','ter_wyzsze','brzeg_wysoczyzny','male_doliny',
            'dno_doliny','stok_doliny','krawedz_doliny','poza_dolinami','rownina',
            'obsz_falisty','obsz_pagorkowaty','obsz_gorzysty','uwagi']

EKSPOZYCJA_ATR = ['id','eksponowany','kraw_stoki','sfaldowania_cyple','cyple_wybitne','waly_garby','wyniesienia_okrezne', 
                'osloniety','podst_stoku','doliny_niecki', 'kotlinki_zagleb','jaskinie','stopien','rozmiar',
                'kierunek','uwagi']
TEREN_ATR=['id','zabudowany','sred_zabud','rolniczy','spoleczny','przemyslowy',
                'las','sad','park','pole_orne','laka','utwor_geo','uwagi']

OBSZAR_ATR = ['id','obserwacja','pole','nasyc_rozklad','nasyc_typ','gestosc_znal','powierzchnia','uwagi']

ZAGROZENIA_ATR=['id','wystepowanie','przyczyna','uzytkownik','uwagi']

WNIOSKI_ATR=['id','wartosc','inwentaryzacja','wykopaliska','interwencja','uwagi']