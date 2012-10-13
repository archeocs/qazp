# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from functools import *
import sqlite3
from lib.qgsop import *
from dane.zrodla import getPolaczenie, daneFizg, updtFizg, daneEksp, updtEkspo,\
    daneTeren, updtTeren, updtObszar, daneObszar, updtZagr, daneZagr, updtWnio,\
    daneWnio
from dane.model import STANOWISKA_ATR
import logging

def conw(w,slow):
    if isinstance(w, QVariant):
        klucz = str(w.toString()).upper()
    else:
        klucz = str(w).upper()
    if slow.has_key(klucz):
        return slow[klucz]
    return None

class Widok(QTableView):
    
    vb = [('T','Tak'),('N','Nie')]
    vr = [('M',u'Mała'),( 'S',u'Średnia'),( 'D',u'Duża')]
    ve = [('I',u'Istnieje'),( 'N',u'Nie istnieje')]
    
    def __init__(self,dane=None,parent=None):
        QTableView.__init__(self,parent)
        self._del = WyborDelegate(parent=self)
        self.setItemDelegate(self._del)
        self.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.AnyKeyPressed)
    
    def dodajOpt(self,r,v):
        self._del.setOpcja(r,v)
        return self
        
    def dodajDb(self,r,d):
        self._del.setDb(r,d)
        return self
    
    def dodTn(self,r):
        self._del.setOpcja(r,self.vb)
    
    def setDelegat(self,opcje,w):
        self.setItemDelegate(WyborDelegate(opcje,parent=self))
        print 'ok'
        
    def ustawModel(self,dane,opcje):
        self.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        if not dane:
            self._dane = {}
        else:
            self._dane = dane
        _mod = PropLista(opcje,self._dane,parent=self)
        self.setModel(_mod)
        self.horizontalHeader().setResizeMode(QHeaderView.Stretch)
    
    def konwert(self, dane):
        rd = {}
        for (k,v) in dane.iteritems():
            if isinstance(v, QVariant):
                if v.isNull():
                    rd[k] = None
                    continue
                t = v.type()
                if t == QVariant.Int:
                    rd[k] = v.toInt()[0]
                elif t == QVariant.Double:
                    rd[k] = v.toDouble()[0]
                elif t == QVariant.DateTime:
                    rd[k] = v.toDateTime().toString(Qt.ISODate)
                elif t == QVariant.DateTime:
                    rd[k] = v.toDate().toString(Qt.ISODate)
                else:
                    rd[k] = unicode(v.toString())
            else:
                rd[k] = unicode(v)
        logging.info('rd '+str(rd))
        return rd
        
    def wartosci(self):
        return self.konwert(self._dane)
    
    wb = partial(conw,slow=dict(vb))
    wr = partial(conw,slow=dict(vr))
    we = partial(conw,slow=dict(ve))
    
    def nic(self,w):
        return w

class Edytor(QFrame):
    def __init__(self,qgsWarstwa,model,win,parent=None):
        QFrame.__init__(self,parent)
        logging.basicConfig(filename='/home/milosz/logqazp.txt', level=logging.INFO)
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
            logging.info('fizgeo')
            dane = panel.wartosci()
            logging.info(str(dane))
            u = updtFizg(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        elif self.on == 'ekspozycja':
            logging.info('ekspozycja')
            dane = panel.wartosci()
            logging.info(str(dane))
            u = updtEkspo(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        elif self.on == 'teren':
            logging.info('teren')
            dane = panel.wartosci()
            logging.info(str(dane))
            u = updtTeren(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        elif self.on == 'obszar':
            logging.info('obszar')
            dane = panel.wartosci()
            logging.info(str(dane))
            u = updtObszar(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        elif self.on == 'zagrozenia':
            logging.info('zagrozenia')
            dane = panel.wartosci()
            logging.info(str(dane))
            u = updtZagr(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        elif self.on == 'wnioski':
            logging.info('wnioski')
            dane = panel.wartosci()
            logging.info(str(dane))
            u = updtWnio(str(self._model['id'].toString()),self._war,[dane])
            self._win.statusBar().showMessage('Zapisany '+self.on+" "+str(u))
        else:
            self._win.statusBar().showMessage(self.on)

    def klikZamknij(self):
        self._win.usun(self)
        
def fdb(ident,war,tab):
    if ident is None:
        return None
    con = getPolaczenie(war)
    cur = con.cursor()
    if isinstance(ident, QVariant):
        sid=str(ident.toString())
    else:
        sid = str(ident)
    if sid == None or sid == '':
        return 'PUSTY'
    try:    
        cur.execute('select nazwa from '+tab+' where id='+sid)
        ret = cur.fetchone()
        cur.close()
        con.close()
        if ret:
            return ret[0]
    except:
        return 'select nazwa from '+tab+' where id='+sid
      
class StanowiskoWidok(Widok):
    vrd = [('P',u'Powierzchniowe'),('W',u'Weryfikacja'),('L',u'Lotnicze')]
    wrd = partial(conw,slow=dict(vrd))
    def __init__(self,qgsWarstwa,dane=None,parent=None):
        Widok.__init__(self,parent)
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
    

class WyborDelegate(QStyledItemDelegate):

    def __init__(self,parent=None):
        QStyledItemDelegate.__init__(self,parent)
        self._opt = {}
        self._con = {}
    
    def setOpcja(self,r,op):
        self._opt[r] = op
        
    def setDb(self,r,con):
        self._con[r] = con
        
    def getDane(self,pc):
        con = getPolaczenie(pc[0])
        cur = con.cursor()
        stmt = 'select id,nazwa from '+pc[1]+' order by nazwa'
        cur.execute(stmt)
        ret = cur.fetchall()
        cur.close()
        con.close()
        return ret  

    def createEditor(self,parent,styl,indeks):
        self.initStyleOption(styl,indeks)
        c = indeks.column()
        if c == 1:
            if self._opt.has_key(indeks.row()):
                tw = self._opt[indeks.row()]
            elif self._con.has_key(indeks.row()):
                tw = self.getDane(self._con[indeks.row()])
            else:
                return QStyledItemDelegate.createEditor(self,parent,styl,indeks)
            cb = QComboBox(parent)
            for o in tw:
                cb.addItem(o[1],o[0])
            cb.addItem(u'Nieokreślone',QVariant())
            return cb
        return None
 
    def setEditorData(self,edytor,indeks):
        di = indeks.data()
        if self._opt.has_key(indeks.row()) or self._con.has_key(indeks.row()):
            for i in range(edytor.count()):
                if edytor.itemText(i) == di:
                    edytor.setCurrentIndex(i)
                    return
            edytor.setCurrentIndex(edytor.count()-1) # wartosc nieokreslona
        else:
            QStyledItemDelegate.setEditorData(self,edytor,indeks)
    
    def setModelData(self,edytor,model,indeks):
        if self._opt.has_key(indeks.row()) or self._con.has_key(indeks.row()):
            d = edytor.itemData(edytor.currentIndex())
            model.setData(indeks,d)
        else:
            model.setData(indeks,QVariant(edytor.text()))

class PropLista(QAbstractTableModel):
    
    def __init__(self,opt,dane,parent=None): # dane = slownik {klucz:wartosc}
        QAbstractTableModel.__init__(self,parent)
        self._opt = opt
        self._dane = dane
        self._wid = {}
        
    def rowCount(self, *args, **kwargs):
        return len(self._opt)
    
    def columnCount(self, *args, **kwargs):
        return 2
    
    def data(self, indeks, rola = Qt.DisplayRole):
        r,c = indeks.row(), indeks.column()
        if rola == Qt.DisplayRole:
            if c == 0:
                return self._opt[r][0]
            elif c == 1 and self._dane.has_key(self._opt[r][1]):
                if not self._wid.has_key(self._opt[r][1]):
                    self._wid[self._opt[r][1]] = self._opt[r][2](self._dane[self._opt[r][1]]) 
                return self._wid[self._opt[r][1]]
        elif rola == Qt.EditRole and c == 1 and self._dane.has_key(self._opt[r][1]):
            if not self._wid.has_key(self._opt[r][1]):
                self._wid[self._opt[r][1]] = self._opt[r][2](self._dane[self._opt[r][1]]) 
            return self._wid[self._opt[r][1]]
        return QVariant()
    
    def setData(self,indeks, wartosc, rola=Qt.EditRole):
        r,c = indeks.row(), indeks.column()
        if rola == Qt.EditRole and c == 1:
            self._dane[self._opt[r][1]] = wartosc
            self._wid.pop(self._opt[r][1],'')
            return True
        return False
            #self.dataChanged(indeks,indeks)
    
    def flags(self,indeks):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable
    
    def headerData(self, sekcja, orientacja, rola = Qt.DisplayRole):
        if orientacja == Qt.Vertical:
            return None
        if sekcja < 0 or sekcja >= 2:
            raise Exception("headerData: indeks %d poza zakresem [0,%d]"%(sekcja,len(self._nag)-1))
        if rola == Qt.DisplayRole:
            if sekcja == 0:
                return u'Nazwa'
            elif sekcja == 1:
                return u'Wartość'

class ObszarWidok(Widok):
    
    vnt = [('J',u'Jednocentryczne'),('W',u'Wielocentryczne'),('D',u'Dekocentryczne')]
    vnr = [('R',u'Równomierny'),( 'N',u'Nierównomierny')]
    vo = [('U',u'Utrudniona'),( 'B',u'Bez przeszkód')]
    vp = [('O',u'Otwarte'),( 'Z',u'Zamknięte')]
    
    wnt = partial(conw,slow=dict(vnt))
    wnr = partial(conw,slow=dict(vnr))
    wo = partial(conw,slow=dict(vo))
    wp = partial(conw,slow=dict(vp))
    
    def __init__(self,dane=None,parent=None):
        Widok.__init__(self,parent)
        opt = [(u'Obserwacja','obserwacja',self.wo),(u'Pole','pole',self.wp), (u'Rozkład nasycenia','nasyc_rozklad',self.wnr),
                (u'Typ nasycenia','nasyc_typ',self.wnt), (u'Gęstość znalezisk','gestosc_znal',self.wr), 
                (u'Powierzchnia','powierzchnia',self.nic)]
        self.ustawModel(dane,opt)
        self.dodajOpt(0,self.vo).dodajOpt(1,self.vp).dodajOpt(2,self.vnr).dodajOpt(3,self.vnt).dodajOpt(4,self.vr)
        #self.setDelegat([(u'Otwarte','O'),(u'Zamknięte','Z')],100)
        
class FizgWidok(Widok):
    
    def __init__(self,dane=None,parent=None):
        Widok.__init__(self,parent)
        opt=[(u'Nadmorska','nadmorska',self.wb),(u'W morzu','w_morzu',self.wb),(u'Plaża','plaza',self.wb),(u'Mierzeja','mierzeja',self.wb),(u'Skarpa','skarpa',self.wb),(u'Wał wydomowy','wal_wydmowy',self.wb),
              (u'Duże doliny','duze_doliny',self.wb),(u'W wodzie','w_wodzie',self.wb),(u'Ter. denna','ter_denna',self.wb),(u'Ter. nadzalewowa','ter_nadzalewowa',self.wb),(u'Ter. wyższe','ter_wyzsze',self.wb),(u'Brzeg wysoczyzny','brzeg_wysoczyzny',self.wb),
              (u'Małe doliny','male_doliny',self.wb),(u'Dno doliny','dno_doliny',self.wb),(u'Stok doliny','stok_doliny',self.wb),(u'Krawędź doliny','krawedz_doliny',self.wb),
              (u'Poza dolinami','poza_dolinami',self.wb),(u'Równina','rownina',self.wb),(u'Obsz. falisty','obsz_falisty',self.wb)
                ,(u'Obsz. pagórkowaty','obsz_pagorkowaty',self.wb),(u'Obsz. górzysty','obsz_gorzysty',self.wb)]
        self.ustawModel(dane,opt)
        for x in range(len(opt)):
            self.dodTn(x)

class TerenWidok(Widok):
    def __init__(self,dane=None,parent=None):
        Widok.__init__(self,parent)
        opt=[(u'Zabudowany','zabudowany',self.wb),(u'Śred. zabudowany','sred_zabud',self.wb),(u'Rolniczy','rolniczy',self.wb),(u'Społeczny','spoleczny',self.wb),(u'Przemysłowy','przemyslowy',self.wb),
                (u'Las','las',self.wb),(u'Sad','sad',self.wb),(u'Park','park',self.wb),(u'Pole orne','pole_orne',self.wb),(u'Łąka','laka',self.wb),(u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        for x in range(len(opt)-1):
            self.dodTn(x)
                
class EkspozycjaWidok(Widok):
    def __init__(self,dane=None,parent=None):
        Widok.__init__(self,parent)
        opt=[(u'Eksponowany','eksponowany',self.wb),(u'Krawędzie, stoki','kraw_stoki',self.wb),(u'Sfałdowania, cyple','sfaldowania_cyple',self.wb),
                (u'Cyple wybitne','cyple_wybitne',self.wb), (u'Wały, garby','waly_garby',self.wb), (u'Wyniesienia okrężne','wyniesienia_okrezne',self.wb), 
                (u'Osłonięty','osloniety',self.wb),(u'Podstawa stoku','podst_stoku',self.wb),(u'Doliny, niecki','doliny_niecki',self.wb), 
                (u'Kotlinki, zagłębienia','kotlinki_zagleb',self.wb), ('Jaskinie','jaskinie',self.wb),(u'Stopień ekspozycji','stopien',self.nic),(u'Rozmiar ekspozycji','rozmiar',self.nic),
                (u'Kierunek ekspozycji','kierunek',self.nic),(u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        for x in range(len(opt)-4):
            self.dodTn(x)
            
class ZagrozenieWidok(Widok):
    vp = [('L',u'Ludzie'),('N',u'Natura')]
    wp = partial(conw,slow=dict(vp))
    vu = [('S',u'Społeczny'),('P',u'Prywatny')]
    wu = partial(conw,slow=dict(vu))
    def __init__(self,dane=None,parent=None):
        Widok.__init__(self,parent)
        opt=[(u'Występowanie','wystepowanie',self.we),(u'Przyczyna','przyczyna',self.wp),(u'Użytkownik','uzytkownik',self.wu),
            (u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        self.dodajOpt(0,self.ve).dodajOpt(1,self.vp).dodajOpt(2,self.vu)
        
class WnioskiWidok(Widok):
    def __init__(self,dane=None,parent=None):
        Widok.__init__(self,parent)
        opt=[(u'Wartość','wartosc',self.wr),(u'Inwentaryzacja','inwentaryzacja',self.wb),(u'Wykopaliska','wykopaliska',self.wb),
            (u'Interwencja','interwencja',self.wb), (u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        self.dodajOpt(0,self.vr).dodajOpt(1,self.vb).dodajOpt(2,self.vb).dodajOpt(3,self.vb)