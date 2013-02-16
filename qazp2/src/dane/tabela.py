# -*- coding: utf-8 -*-

# (c) Milosz Piglas 2013 Wszystkie prawa zastrzezone

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

TAKNIEATR = [('T', 'Tak'), ('N', 'Nie')]

class Atrybut(object):

    def __init__(self, nazwa, dozwolone=None, etykieta=None): # jezeli dowolone == None to znaczy ze kazda wartosc jest dozwolona
        self._nazwa = nazwa
        self._dozwolone = dozwolone
        self._etykieta = etykieta
    
    @property    
    def anazwa(self):
        return self._nazwa
    
    @property
    def dozwolone(self): # zwraca etykiety dozwolonych wartosci
        if self._dozwolone is not None:
            return [d[1] for d in self._dozwolone]
        return None
    
    def dodajKod(self, symbol, etykieta):
        if self._dozwolone is None:
            self._dozwolone = []
        self._dozwolone.append((symbol, etykieta))
        return self
    
    def kodwar(self, i):
        return self._dozwolone[i][0]
    
    def etwar(self, i):
        return self._dozwolone[i][1]

    @property    
    def aetykieta(self):
        return self._etykieta

    def __unicode__(self):
        return self._etykieta

def atrsTab(tab):
    atrs = []
    for t in tab:
        atrs.append(Atrybut(t[0], t[1], t[2]))
    return atrs

class Tabela(object):
    
    def __init__(self, nazwa, atrybuty, etykieta=None):
        self._nazwa = nazwa
        self._atrs = atrybuty
        self._etykieta = etykieta
    
    @property    
    def tnazwa(self):
        return self._nazwa
    
    @property
    def atrs(self):
        return self._atrs

    @property
    def tetykieta(self):
        return self._etykieta
    
    def dodajAtr(self, nazwa, etykieta, dozwolone=None):
        a = Atrybut(nazwa, etykieta=etykieta, dozwolone=dozwolone)
        self._atrs.append(a)
        return a

def fizgeo():
    t = Tabela('fizgeo_dane', [], 'Jed. fiz.-geo.')
    t.dodajAtr('nadmorska', u'Nadmorska', TAKNIEATR)
    t.dodajAtr('w_morzu', u'W morzu', TAKNIEATR)
    t.dodajAtr('plaza', u'Plaża', TAKNIEATR)
    t.dodajAtr('mierzeja', u'Mierzeja', TAKNIEATR)
    t.dodajAtr('skarpa', u'Skarpa', TAKNIEATR)
    t.dodajAtr('wal_wydmowy', u'Wał wydmowy', TAKNIEATR)
    t.dodajAtr('duze_doliny', u'Duże doliny', TAKNIEATR)
    t.dodajAtr('w_wodzie', u'W wodzie', TAKNIEATR)
    t.dodajAtr('ter_denna', u'Ter. denna', TAKNIEATR)
    t.dodajAtr('ter_nadzalewowa', u'Ter. nadzalewowa', TAKNIEATR)
    t.dodajAtr('ter_wyzsze', u'Ter. wyższe', TAKNIEATR)
    t.dodajAtr('brzeg_wysoczyzny', u'Brzeg wysoczyzny', TAKNIEATR)
    t.dodajAtr('male_doliny', u'Małe doliny', TAKNIEATR)
    t.dodajAtr('dno_doliny', u'Dno doliny', TAKNIEATR)
    t.dodajAtr('stok_doliny', u'Stok doliny', TAKNIEATR)
    t.dodajAtr('krawedz_doliny', u'Krawędź doliny', TAKNIEATR)
    t.dodajAtr('poza_dolinami', u'Poza dolinami', TAKNIEATR)
    t.dodajAtr('rownina', u'Równina', TAKNIEATR)
    t.dodajAtr('obsz_falisty', u'Obsz. falisty', TAKNIEATR)
    t.dodajAtr('obsz_pagorkowaty', u'Obsz. pagórkowaty', TAKNIEATR)
    t.dodajAtr('obsz_gorzysty', u'Obsz. górzysty', TAKNIEATR)
    return t

def obszar():
    t = Tabela('obszar_dane', [], 'Obszar')
    t.dodajAtr('obserwacja', u'Obserwacja')\
        .dodajKod('U', u'Utrudniona')\
        .dodajKod('B', u'Bez przeszkód')
    t.dodajAtr('pole', 'Pole')\
        .dodajKod('O', 'Otwarte')\
        .dodajKod('Z', u'Zamknięte')
    t.dodajAtr('nasyc_rozklad', u'Rozkład nasycenia')\
        .dodajKod('R', u'Równomierny')\
        .dodajKod('N', u'Nierównomierny')
    t.dodajAtr('nasyc_typ', u'Typ nasycenia')\
        .dodajKod('J', u'Jednocentryczny')\
        .dodajKod('W', u'Wielocentryczne')\
        .dodajKod('D', u'Dekocentryczne')
    t.dodajAtr('gestosc_znal', u'Gęstość znalezisk')\
        .dodajKod('M', u'Mała')\
        .dodajKod('S', u'Średnia')\
        .dodajKod('D', u'Duża')
    return t

def teren():
    t = Tabela('teren_dane', [], 'Teren')
    t.dodajAtr('zabudowany', u'Zabudowany', TAKNIEATR)
    t.dodajAtr('sred_zabud', u'Śred. zabudowany', TAKNIEATR)
    t.dodajAtr('prywatny', u'Prywatny', TAKNIEATR)
    t.dodajAtr('spoleczny', u'Społeczny', TAKNIEATR)
    t.dodajAtr('przemyslowy', u'Przemysłowy', TAKNIEATR)
    t.dodajAtr('nieuzytek', u'Nieużytek', TAKNIEATR)
    t.dodajAtr('las', u'Las', TAKNIEATR)
    t.dodajAtr('sad', u'Sad', TAKNIEATR)
    t.dodajAtr('park', u'Park', TAKNIEATR)
    t.dodajAtr('pole_orne', u'Pole orne', TAKNIEATR)
    t.dodajAtr('laka', u'Łąka', TAKNIEATR)
    t.dodajAtr('torf', u'Torf', TAKNIEATR)
    t.dodajAtr('woda', u'Woda', TAKNIEATR)
    t.dodajAtr('bagno', u'Bagno', TAKNIEATR)
    return t

def gleba():
    t = Tabela('gleba_dane', [], 'Gleba')
    t.dodajAtr('luzna', u'Luźna', TAKNIEATR)
    t.dodajAtr('zwiezla', u'Zwięzła', TAKNIEATR)
    t.dodajAtr('torf_bag', u'Torf.-bag', TAKNIEATR)
    t.dodajAtr('kamienistosc', u'Kamienistość')\
        .dodajKod('M', u'Mała')\
        .dodajKod('S', u'Średnia')\
        .dodajKod('D', u'Duża')
    return t
    
def wnioski():
    t = Tabela('wnioski', [], 'Wnioski')
    t.dodajAtr('wartosc', u'Wartość')\
        .dodajKod('M', u'Mała')\
        .dodajKod('S', u'Średnia')\
        .dodajKod('D', u'Duża')
    t.dodajAtr('inwentaryzacja', u'Inwentaryzacja', TAKNIEATR)
    t.dodajAtr('interwencja', u'Interwencja', TAKNIEATR)
    t.dodajAtr('wykopaliska', u'Wykopaliska', TAKNIEATR)
    return t
        
def ekspozycja():
    t = Tabela('ekspozycja_dane', [], 'Ekspozycja')
    t.dodajAtr('eksponowany', u'Eksponowany', TAKNIEATR)
    t.dodajAtr('kraw_stoki', u'Krawędzie, stoki', TAKNIEATR)
    t.dodajAtr('sfaldowania_cyple', u'Sfałdowania, cyple', TAKNIEATR)
    t.dodajAtr('cyple_wybitne', u'Cyple wybitne', TAKNIEATR)
    t.dodajAtr('waly_garby', u'Wały, garby', TAKNIEATR)
    t.dodajAtr('wyniesienia_okrezne', u'Wyniesienia okrężne', TAKNIEATR)
    t.dodajAtr('osloniety', u'Osłonięty', TAKNIEATR)
    t.dodajAtr('podst_stoku', u'Podstawa stoku', TAKNIEATR)
    t.dodajAtr('doliny_niecki', u'Doliny, niecki', TAKNIEATR)
    t.dodajAtr('kotlinki_zagleb', u'Kotlinki, zagłębienia', TAKNIEATR)
    t.dodajAtr('jaskinie', u'Jaskinie', TAKNIEATR)
    t.dodajAtr('stopien', u'Stopień')
    t.dodajAtr('rozmiar', u'Rozmiar')
    t.dodajAtr('kierunek', u'Kierunek')
    return t

def zagrozenia():
    t = Tabela('zagrozenia', [], u'Zagrożenia')
    t.dodajAtr('wystepowanie', u'Występowanie')\
        .dodajKod('I', 'Istnieje')\
        .dodajKod('N', 'Nie istnieje')
    t.dodajAtr('czas', 'Czas')\
        .dodajKod('S', u'Stałe')\
        .dodajKod('D', u'Doraźne')
    t.dodajAtr('przyczyna_ludzie', u'Przyczyna:Ludzie', TAKNIEATR)
    t.dodajAtr('przyczyna_natura', u'Przyczyna:Natura', TAKNIEATR)
    t.dodajAtr('uzytkownik_spoleczny', u'Użytkownik pryw.', TAKNIEATR)
    t.dodajAtr('uzytkownik_prywatny', u'Użytkownik społ.', TAKNIEATR)
    return t