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

from PyQt4.QtGui import QDialogButtonBox, QFrame, QGridLayout
from PyQt4.QtCore import Qt, QVariant
from functools import partial
from lib.qgsop import setMapa,zmien
from dane.zrodla import getPolaczenie2, daneFizg, updtFizg, daneEksp, updtEkspo,\
    daneTeren, updtTeren, updtObszar, daneObszar, updtZagr, daneZagr, updtWnio,\
    daneWnio
from dane.model import STANOWISKA_ATR
from widok.proped import conw, PropWidok



class Edytor(QFrame):
    def __init__(self,qgsWarstwa,model,win,parent=None):
        QFrame.__init__(self,parent)
        #logging.basicConfig(filename='logqazp.txt', level=logging.INFO)
        self._win = win
        self._model = model
        self._war = qgsWarstwa
        self.grid = QGridLayout(self)
        self.setLayout(self.grid)
        pbb = QDialogButtonBox(Qt.Vertical,self)
        pbb.addButton('Stanowisko',QDialogButtonBox.ActionRole).setObjectName('stanowisko')
        pbb.addButton('Jed. fiz-geo',QDialogButtonBox.ActionRole).setObjectName('fizgeo')
        pbb.addButton('Ekspozycja',QDialogButtonBox.ActionRole).setObjectName('ekspozycja')
        pbb.addButton('Teren',QDialogButtonBox.ActionRole).setObjectName('teren')
        pbb.addButton('Obszar',QDialogButtonBox.ActionRole).setObjectName('obszar')
        pbb.addButton(u'Zagrożenia',QDialogButtonBox.ActionRole).setObjectName('zagrozenia')
        pbb.addButton(u'Wnioski',QDialogButtonBox.ActionRole).setObjectName('wnioski')
        self.grid.addWidget(pbb,0,1)
        bb = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close, parent=self)
        self.grid.addWidget(bb,1,0)
        self.on = 'stanowisko'
        self.grid.addWidget(StanowiskoWidok(self._war,model),0,0) # zamiast informacje o stanowisku
        self.grid.setRowMinimumHeight(0,150)
        self.grid.setColumnMinimumWidth(0,150)
        pbb.clicked.connect(self.klik_pbtn)
        bb.accepted.connect(self.klikZapisz)
        bb.rejected.connect(self.klikZamknij)
        
    def klik_pbtn(self,btn):
        biez = self.grid.itemAtPosition(0,0).widget()
        biez.setParent(None)
        self.grid.removeWidget(biez)
        del biez
        self.on = str(btn.objectName())
        if self.on == 'fizgeo':
            self.grid.addWidget(FizgWidok(daneFizg(str(self._model['id'].toString()),self._war)),0,0) 
        elif self.on == 'teren':
            self.grid.addWidget(TerenWidok(daneTeren(str(self._model['id'].toString()),self._war)),0,0)
        elif self.on == 'ekspozycja':
            self.grid.addWidget(EkspozycjaWidok(daneEksp(str(self._model['id'].toString()),self._war)),0,0)
        elif self.on == 'obszar':
            self.grid.addWidget(ObszarWidok(daneObszar(str(self._model['id'].toString()),self._war)),0,0) 
        elif self.on == 'zagrozenia':
            self.grid.addWidget(ZagrozenieWidok(daneZagr(str(self._model['id'].toString()),self._war)),0,0)
        elif self.on == 'wnioski':
            self.grid.addWidget(WnioskiWidok(daneWnio(str(self._model['id'].toString()),self._war)),0,0) 
        elif self.on == 'stanowisko':   
            self.grid.addWidget(StanowiskoWidok(self._war,self._model),0,0)
            
    def klikZapisz(self):
        panel = self.grid.itemAtPosition(0,0).widget()
        #print panel.wartosci()
        if self.on == 'stanowisko':
            obj = self._model.feature()
            setMapa(obj, panel.wartosci(), STANOWISKA_ATR)
            if zmien(self._war,obj):
                self._win.statusBar().showMessage('Zapisano zmiany')
            else:
                self._win.statusBar().showMessage('Blad zapisu')
        elif self.on == 'fizgeo':
            dane = panel.wartosci()
            u = updtFizg(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        elif self.on == 'ekspozycja':
            dane = panel.wartosci()
            u = updtEkspo(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        elif self.on == 'teren':
            dane = panel.wartosci()
            u = updtTeren(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        elif self.on == 'obszar':
            dane = panel.wartosci()
            u = updtObszar(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        elif self.on == 'zagrozenia':
            dane = panel.wartosci()
            u = updtZagr(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        elif self.on == 'wnioski':
            dane = panel.wartosci()
            u = updtWnio(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        else:
            self._win.statusBar().showMessage(self.on)

    def klikZamknij(self):
        self._win.usun(self)
        
def fdb(ident,war,tab):
    if ident is None:
        return None
    if isinstance(ident, QVariant):
        sid=str(ident.toString())
    else:
        sid = str(ident)
    if sid == None or sid == '':
        return 'PUSTY'
    try:    
        con = getPolaczenie2(war)
        ret = con.jeden('select nazwa from '+tab+' where id=#',[sid])
        con.zakoncz()
        if ret:
            return ret[0]
    except:
        return 'select nazwa from '+tab+' where id='+sid
      
class StanowiskoWidok(PropWidok):
    vrd = [('P',u'Powierzchniowe'),('W',u'Weryfikacja'),('L',u'Lotnicze')]
    wrd = partial(conw,slow=dict(vrd))
    def __init__(self,qgsWarstwa,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        mdb = partial(fdb,war=qgsWarstwa,tab='miejscowosci')
        gdb = partial(fdb,war=qgsWarstwa,tab='gminy')
        pdb = partial(fdb,war=qgsWarstwa,tab='powiaty')
        wdb = partial(fdb,war=qgsWarstwa,tab='wojewodztwa')
        opt=[(u'Obszar','obszar',self.nic),(u'Nr na obszarze','nr_obszar',self.nic),(u'Miejscowość','miejscowosc',mdb),
             (u'Nr w miejscowości','nr_miejscowosc',self.nic),(u'Gmina','gmina',gdb),(u'Powiat','powiat',pdb),
             (u'Województwo','wojewodztwo',wdb),(u'Rodzaj','rodzaj_badan',self.wrd),('Data','data',self.nic),
             (u'Autor','autor',self.nic),(u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        self.dodajOpt(7, self.vrd)
        self.dodajDb(2,(qgsWarstwa,'miejscowosci')).dodajDb(4,(qgsWarstwa,'gminy')).dodajDb(5,(qgsWarstwa,'powiaty')).dodajDb(6,(qgsWarstwa,'wojewodztwa'))
    
    mk = {'miejscowosc':int, 'gmina':int, 'powiat':int, 'wojewodztwo':int}
    

class ObszarWidok(PropWidok):
    
    vnt = [('J',u'Jednocentryczne'),('W',u'Wielocentryczne'),('D',u'Dekocentryczne')]
    vnr = [('R',u'Równomierny'),( 'N',u'Nierównomierny')]
    vo = [('U',u'Utrudniona'),( 'B',u'Bez przeszkód')]
    vp = [('O',u'Otwarte'),( 'Z',u'Zamknięte')]
    
    wnt = partial(conw,slow=dict(vnt))
    wnr = partial(conw,slow=dict(vnr))
    wo = partial(conw,slow=dict(vo))
    wp = partial(conw,slow=dict(vp))
    
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt = [(u'Obserwacja','obserwacja',self.wo),(u'Pole','pole',self.wp), (u'Rozkład nasycenia','nasyc_rozklad',self.wnr),
                (u'Typ nasycenia','nasyc_typ',self.wnt), (u'Gęstość znalezisk','gestosc_znal',self.wr), 
                (u'Powierzchnia','powierzchnia',self.nic)]
        self.ustawModel(dane,opt)
        self.dodajOpt(0,self.vo).dodajOpt(1,self.vp).dodajOpt(2,self.vnr).dodajOpt(3,self.vnt).dodajOpt(4,self.vr)
        #self.setDelegat([(u'Otwarte','O'),(u'Zamknięte','Z')],100)
        
class FizgWidok(PropWidok):
    
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Nadmorska','nadmorska',self.wb),(u'W morzu','w_morzu',self.wb),(u'Plaża','plaza',self.wb),(u'Mierzeja','mierzeja',self.wb),(u'Skarpa','skarpa',self.wb),(u'Wał wydomowy','wal_wydmowy',self.wb),
              (u'Duże doliny','duze_doliny',self.wb),(u'W wodzie','w_wodzie',self.wb),(u'Ter. denna','ter_denna',self.wb),(u'Ter. nadzalewowa','ter_nadzalewowa',self.wb),(u'Ter. wyższe','ter_wyzsze',self.wb),(u'Brzeg wysoczyzny','brzeg_wysoczyzny',self.wb),
              (u'Małe doliny','male_doliny',self.wb),(u'Dno doliny','dno_doliny',self.wb),(u'Stok doliny','stok_doliny',self.wb),(u'Krawędź doliny','krawedz_doliny',self.wb),
              (u'Poza dolinami','poza_dolinami',self.wb),(u'Równina','rownina',self.wb),(u'Obsz. falisty','obsz_falisty',self.wb)
                ,(u'Obsz. pagórkowaty','obsz_pagorkowaty',self.wb),(u'Obsz. górzysty','obsz_gorzysty',self.wb)]
        self.ustawModel(dane,opt)
        for x in range(len(opt)):
            self.dodTn(x)

class TerenWidok(PropWidok):
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Zabudowany','zabudowany',self.wb),(u'Śred. zabudowany','sred_zabud',self.wb),(u'Rolniczy','rolniczy',self.wb),(u'Społeczny','spoleczny',self.wb),(u'Przemysłowy','przemyslowy',self.wb),
                (u'Las','las',self.wb),(u'Sad','sad',self.wb),(u'Park','park',self.wb),(u'Pole orne','pole_orne',self.wb),(u'Łąka','laka',self.wb),(u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        for x in range(len(opt)-1):
            self.dodTn(x)
                
class EkspozycjaWidok(PropWidok):
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Eksponowany','eksponowany',self.wb),(u'Krawędzie, stoki','kraw_stoki',self.wb),(u'Sfałdowania, cyple','sfaldowania_cyple',self.wb),
                (u'Cyple wybitne','cyple_wybitne',self.wb), (u'Wały, garby','waly_garby',self.wb), (u'Wyniesienia okrężne','wyniesienia_okrezne',self.wb), 
                (u'Osłonięty','osloniety',self.wb),(u'Podstawa stoku','podst_stoku',self.wb),(u'Doliny, niecki','doliny_niecki',self.wb), 
                (u'Kotlinki, zagłębienia','kotlinki_zagleb',self.wb), ('Jaskinie','jaskinie',self.wb),(u'Stopień ekspozycji','stopien',self.nic),(u'Rozmiar ekspozycji','rozmiar',self.nic),
                (u'Kierunek ekspozycji','kierunek',self.nic),(u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        for x in range(len(opt)-4):
            self.dodTn(x)
            
class ZagrozenieWidok(PropWidok):
    vp = [('L',u'Ludzie'),('N',u'Natura')]
    wp = partial(conw,slow=dict(vp))
    vu = [('S',u'Społeczny'),('P',u'Prywatny')]
    wu = partial(conw,slow=dict(vu))
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Występowanie','wystepowanie',self.we),(u'Przyczyna','przyczyna',self.wp),(u'Użytkownik','uzytkownik',self.wu),
            (u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        self.dodajOpt(0,self.ve).dodajOpt(1,self.vp).dodajOpt(2,self.vu)
        
class WnioskiWidok(PropWidok):
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Wartość','wartosc',self.wr),(u'Inwentaryzacja','inwentaryzacja',self.wb),(u'Wykopaliska','wykopaliska',self.wb),
            (u'Interwencja','interwencja',self.wb), (u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        self.dodajOpt(0,self.vr).dodajOpt(1,self.vb).dodajOpt(2,self.vb).dodajOpt(3,self.vb)