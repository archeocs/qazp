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

from PyQt4.QtGui import QDialogButtonBox, QFrame, QGridLayout,QWidget,QVBoxLayout,QHBoxLayout,\
                        QLabel, QPushButton, QFileDialog, QPixmap, QShortcut, QKeySequence
from PyQt4.QtCore import Qt, QVariant
from functools import partial
from lib.qgsop import setMapa,zmien
from dane.zrodla import getPolaczenie2, daneFizg, updtFizg, daneEksp, updtEkspo,\
    daneTeren, updtTeren, updtObszar, daneObszar, updtZagr, daneZagr, updtWnio,\
    daneWnio, daneGleba, updtGleba, daneAkt, updtAkt, daneKarta, updtKarta
from dane.model import STANOWISKA_ATR
from widok.proped import conw, PropWidok
from widok.faktyed import FaktyWidok
from lib.media import odczyt, zapiszMapa, usunMapa
from lib.uzytki import sprSchemat



class Edytor(QFrame):
    def __init__(self, qgsWarstwa, model, win, funModel=None, parent=None):
        QFrame.__init__(self, parent)
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
        pbb.addButton('Gleba',QDialogButtonBox.ActionRole).setObjectName('gleba')
        pbb.addButton('Obszar',QDialogButtonBox.ActionRole).setObjectName('obszar')
        pbb.addButton(u'Zagrożenia',QDialogButtonBox.ActionRole).setObjectName('zagrozenia')
        pbb.addButton(u'Wnioski',QDialogButtonBox.ActionRole).setObjectName('wnioski')
        pbb.addButton(u'Aktualnosci',QDialogButtonBox.ActionRole).setObjectName('aktualnosci')
        pbb.addButton(u'Karta',QDialogButtonBox.ActionRole).setObjectName('karta')
        pbb.addButton(u'Fakty',QDialogButtonBox.ActionRole).setObjectName('fakty')
        pbb.addButton(u'Mapa',QDialogButtonBox.ActionRole).setObjectName('mapa')
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
        self._funModel = funModel
        if self._funModel is not None:
            bb.addButton(u'Poprzednie (Ctrl+P)', QDialogButtonBox.ActionRole).clicked.connect(self.klikPoprzedni)
            QShortcut(QKeySequence(Qt.CTRL+Qt.Key_P),self._win).activated.connect(self.klikPoprzedni)
            bb.addButton(u'Następne (Ctrl+N)', QDialogButtonBox.ActionRole).clicked.connect(self.klikNastepny)
            QShortcut(QKeySequence(Qt.CTRL+Qt.Key_N),self._win).activated.connect(self.klikNastepny)
    
    def _zmienModel(self, model):
        self._model = model
        self.zmienPanel(self.on)
        self._win.setWindowTitle('Stanowisko: '+str(model['obszar'].toString())+'/'+str(model['nr_obszar'].toString()))
            
    def klikPoprzedni(self):
        m = self._funModel(-1)
        if m is not None:
            self._zmienModel(m)
            
    def klikNastepny(self):   
        m = self._funModel(1)
        if m is not None:
            self._zmienModel(m)
        
    def zmienPanel(self, panel):
        biez = self.grid.itemAtPosition(0,0).widget()
        if self.on == 'fakty':
            biez.wycofaj() 
        biez.setParent(None)
        self.grid.removeWidget(biez)
        del biez
        self.on = panel #str(btn.objectName())
        if self.on == 'fizgeo':
            self.grid.addWidget(FizgWidok(daneFizg(str(self._model['id'].toString()),self._war)),0,0) 
        elif self.on == 'teren':
            self.grid.addWidget(TerenWidok(daneTeren(str(self._model['id'].toString()),self._war)),0,0)
        elif self.on == 'gleba':
            self.grid.addWidget(GlebaWidok(daneGleba(str(self._model['id'].toString()),self._war)),0,0)
        elif self.on == 'ekspozycja':
            self.grid.addWidget(EkspozycjaWidok(daneEksp(str(self._model['id'].toString()),self._war)),0,0)
        elif self.on == 'obszar':
            self.grid.addWidget(ObszarWidok(daneObszar(str(self._model['id'].toString()),self._war)),0,0) 
        elif self.on == 'zagrozenia':
            self.grid.addWidget(ZagrozenieWidok(daneZagr(str(self._model['id'].toString()),self._war)),0,0)
        elif self.on == 'wnioski':
            self.grid.addWidget(WnioskiWidok(daneWnio(str(self._model['id'].toString()),self._war)),0,0) 
        elif self.on == 'aktualnosci':
            self.grid.addWidget(AktualnosciWidok(daneAkt(str(self._model['id'].toString()),self._war)),0,0) 
        elif self.on == 'karta':
            self.grid.addWidget(KartaWidok(daneKarta(str(self._model['id'].toString()),self._war)),0,0) 
        elif self.on == 'stanowisko':   
            self.grid.addWidget(StanowiskoWidok(self._war,self._model),0,0)
        elif self.on == 'fakty':
            self.grid.addWidget(faktyWidok(str(self._model['id'].toString()),self._war),0,0) 
        elif self.on == 'mapa':
            con = getPolaczenie2(self._war)
            if sprSchemat(con, '0001')[0]:
                self.grid.addWidget(MapaWidok(str(self._model['id'].toString()),self._war),0,0)
            else:
                self._win.statusBar().showMessage('Nieaktualny schemat bazy danych')
            con.zakoncz() 
        
    def klik_pbtn(self,btn):
        self.zmienPanel(str(btn.objectName()))
            
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
        elif self.on == 'gleba':
            dane = panel.wartosci()
            u = updtGleba(str(self._model['id'].toString()),self._war,[dane])
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
        elif self.on == 'aktualnosci':
            dane = panel.wartosci()
            u = updtAkt(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        elif self.on == 'karta':
            dane = panel.wartosci()
            u = updtKarta(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        elif self.on == 'fakty':
            panel.zatwierdz()
        elif self.on == 'mapa':
            panel.zatwierdz()
        else:
            self._win.statusBar().showMessage(self.on)

    def klikZamknij(self):
        if self.on == 'fakty':
            self.grid.itemAtPosition(0,0).widget().wycofaj()    
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
        ret = con.jeden('select nazwa from '+tab+' where id=?',[sid])
        con.zakoncz()
        if ret:
            return ret[0]
    except:
        return 'select nazwa from '+tab+' where id='+sid
      
class StanowiskoWidok(PropWidok):
    vrd = [('P',u'Powierzchniowe'),('W',u'Weryfikacja'),('L',u'Luźne')]
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
                (u'Powierzchnia','powierzchnia',self.nic),(u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        self.dodajOpt(0,self.vo).dodajOpt(1,self.vp).dodajOpt(2,self.vnr).dodajOpt(3,self.vnt).dodajOpt(4,self.vr)
        
class FizgWidok(PropWidok):
    
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Nadmorska','nadmorska',self.wb),(u'W morzu','w_morzu',self.wb),(u'Plaża','plaza',self.wb),(u'Mierzeja','mierzeja',self.wb),(u'Skarpa','skarpa',self.wb),(u'Wał wydomowy','wal_wydmowy',self.wb),
              (u'Duże doliny','duze_doliny',self.wb),(u'W wodzie','w_wodzie',self.wb),(u'Ter. denna','ter_denna',self.wb),(u'Ter. nadzalewowa','ter_nadzalewowa',self.wb),(u'Ter. wyższe','ter_wyzsze',self.wb),(u'Brzeg wysoczyzny','brzeg_wysoczyzny',self.wb),
              (u'Małe doliny','male_doliny',self.wb),(u'Dno doliny','dno_doliny',self.wb),(u'Stok doliny','stok_doliny',self.wb),(u'Krawędź doliny','krawedz_doliny',self.wb),
              (u'Poza dolinami','poza_dolinami',self.wb),(u'Równina','rownina',self.wb),(u'Obsz. falisty','obsz_falisty',self.wb)
                ,(u'Obsz. pagórkowaty','obsz_pagorkowaty',self.wb),(u'Obsz. górzysty','obsz_gorzysty',self.wb),(u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        for x in range(len(opt)-1):
            self.dodTn(x)

class TerenWidok(PropWidok):
    
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Zabudowany','zabudowany',self.wb),(u'Śred. zabudowany','sred_zabud',self.wb),(u'Prywatny','prywatny',self.wb),
             (u'Społeczny','spoleczny',self.wb),(u'Przemysłowy','przemyslowy',self.wb),(u'Nieużytek','nieuzytek',self.wb),
                (u'Las','las',self.wb),(u'Sad','sad',self.wb),(u'Park','park',self.wb),(u'Pole orne','pole_orne',self.wb),
                (u'Łąka','laka',self.wb),(u'Torf','torf',self.wb),(u'Woda','woda',self.wb),(u'Bagno','bagno',self.wb),
                (u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        for x in range(len(opt)-1):
            self.dodTn(x)

class GlebaWidok(PropWidok):
    
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Luźna','luzna',self.wb),(u'Zwięzła','zwiezla',self.wb),(u'Torf.-bag','torf_bag',self.wb),
             (u'Kamienistość','kamienistosc',self.wr) ,(u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        for x in range(len(opt)-2):
            self.dodTn(x)
        self.dodajOpt(3,self.vr)
                
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
    #vp = [('L',u'Ludzie'),('N',u'Natura')]
    #wp = partial(conw,slow=dict(vp))
    #vu = [('S',u'Społeczny'),('P',u'Prywatny')]
    #wu = partial(conw,slow=dict(vu))
    vc = [('S',u'Stałe'),('D',u'Doraźne')]
    wc = partial(conw,slow=dict(vc))
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Występowanie','wystepowanie',self.we),(u'Czas','czas',self.wc),(u'Przyczyna:Ludzie','przyczyna_ludzie',self.wb),
             (u'Przyczyna:Natura','przyczyna_natura',self.wb), (u'Użytkownik społeczny','uzytkownik_spoleczny',self.wb),
             (u'Użytkownik prywatny','uzytkownik_prywatny',self.wb),      (u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        self.dodajOpt(0,self.ve).dodajOpt(1,self.vc).dodajOpt(2,self.vb).dodajOpt(3,self.vb).dodajOpt(4,self.vb).dodajOpt(5,self.vb)
        
class WnioskiWidok(PropWidok):
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Wartość','wartosc',self.wr),(u'Inwentaryzacja','inwentaryzacja',self.wb),(u'Wykopaliska','wykopaliska',self.wb),
            (u'Interwencja','interwencja',self.wb), (u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        self.dodajOpt(0,self.vr).dodajOpt(1,self.vb).dodajOpt(2,self.vb).dodajOpt(3,self.vb)

class AktualnosciWidok(PropWidok):
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Materiały znajdują się w','magazyn',self.nic),(u'Nr inwentarza','nr_inwentarza',self.nic),(u'Rejestr zabytków','nr_krz',self.nic),
            (u'Data rejestracji','data_krz',self.nic), (u'Park kulturowy','park',self.nic), (u'Plan zagospodarowania','plan',self.nic),
             (u'Właściciel','wlasciciel',self.nic), (u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)

class KartaWidok(PropWidok):
    def __init__(self,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Nazwa lokalna','nazwa_lok',self.nic),(u'Arkusz mapy','arkusz_mapy',self.nic),(u'Dalsze losy','dalsze_losy',self.nic),
            (u'Dzieje badań','dzieje_badan',self.nic), (u'Metryka historyczna','metryka_hist',self.nic), (u'Literatura','literatura',self.nic),
             (u'Nr działki geod.','dzialka_geodezyjna',self.nic), (u'Identyfikator EGB','egb',self.nic), (u'Autorzy','autorzy',self.nic),  
             (u'Określił chronologię','chronologia',self.nic),(u'Sprawdził','konsultant',self.nic),  (u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)

class MapaWidok(QWidget):
    
    def __init__(self, st, qgsWarstwa, parent=None):
        QWidget.__init__(self, parent=parent)
        self._st = int(st)
        self._con = getPolaczenie2(qgsWarstwa)
        box = QVBoxLayout()
        self._lbImg = QLabel()
        panelBtn = QWidget()
        layBtn = QHBoxLayout()
        btnDodaj, btnUsun = QPushButton(u'Dodaj'), QPushButton(u'Usuń')
        layBtn.addWidget(btnDodaj)
        layBtn.addWidget(btnUsun)
        btnDodaj.clicked.connect(self._dodajImg)
        btnUsun.clicked.connect(self._usunImg)
        panelBtn.setLayout(layBtn)
        self.setLayout(box)
        box.addWidget(self._lbImg)
        box.addWidget(panelBtn)
        self._mapaId = -1
        self._odswiezImg()
    
    def zatwierdz(self):
        self._con.zatwierdz()
        self._con.zakoncz()
    
    def _dodajImg(self):
        if self._mapaId > 0:
            return
        plik = QFileDialog.getOpenFileName(parent=self, filter='Grafika (*.png *.jpg *.bmp *.tiff *.gif *.jpeg)')
        if plik is None:
            return
        syg = 'MAPA/%d'%self._st
        p = str(plik)
        fi = p.index('.')
        format = None
        if fi > 0 and fi < len(p)-1:
            format = p[fi+1:].upper()
        if zapiszMapa(p, self._st, syg, self._con,format):
            self._odswiezImg() 
    
    def _usunImg(self):
        if self._mapaId <= 0:
            return
        if usunMapa(self._st, self._mapaId, self._con):
            self._odswiezImg()
            
    def _odswiezImg(self):
        ps = self._con.prep("select medium from st_media where stanowisko=? and typ='M'")
        r = ps.jeden([self._st])
        if r is None:
            self._lbImg.setText(u'Brak mapy stanowiska')
            self._mapaId = -1
            return
        img = odczyt(r[0], self._con)
        if img is None:
            self._lbImg.setText(u'Brak mapy stanowiska')
            self._mapaId = -1
            return
        dx,dy = img.dotsPerMeterX(), img.dotsPerMeterY()
        nw = (12 * dx) / 100 # nowa szerokosc wg wzor szer w cm / (100 / dx )
        nh = (12 * dy) / 100
        img = img.scaled(nw,nh,Qt.KeepAspectRatio)
        pm = QPixmap.fromImage(img)
        self._lbImg.setPixmap(pm)
        self._mapaId = r[0]

def faktyWidok(st,warstwa,parent=None):
    return FaktyWidok(st,getPolaczenie2(warstwa),parent)