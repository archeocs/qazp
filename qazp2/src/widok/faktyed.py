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

from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant
from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QLayout, QWidget, \
                        QLabel, QLineEdit,QComboBox, QHeaderView, QTableView, \
                        QPushButton,QMessageBox
                        
from lib.fkwykazy import KodyWykaz, WykazFaktow
from functools import partial

class ListaFaktow(QAbstractTableModel):

    def __init__(self,fakty, parent=None):
        QAbstractTableModel.__init__(self)
        self._fk = fakty
       
    def rowCount(self, *args, **kwargs):
        return len(self._fk)+1
   
    def columnCount(self, *args, **kwargs):
        return 5
       
    def data(self, indeks, rola = Qt.DisplayRole):
        if rola == Qt.DisplayRole and indeks.row() < len(self._fk):
            return QVariant(self._fk.widok(indeks.row(), indeks.column()))
        return QVariant()
    
    NAGLOWKI = [u'Chronologia',u'Kultura',u'Funkcja',u'Masowy',u'Wydzielone']
    def headerData(self, sekcja, orientacja, rola = Qt.DisplayRole):
        if orientacja == Qt.Vertical:
            return None
        if rola == Qt.DisplayRole:
            if sekcja < 7:
                return self.NAGLOWKI[sekcja]
        return QVariant()
    
def funWykaz(con):
    return KodyWykaz(con,'funkcje')

def jedWykaz(con):
    return KodyWykaz(con,'jednostki')

def okrWykaz(con):
    return KodyWykaz(con,'okresy_dziejow')        

def lwgt(widgety,box,marg=0):
    nwgt = QWidget()
    box.setSizeConstraint(QLayout.SetMinimumSize)
    box.setContentsMargins(marg,marg,marg,marg)
    for w in widgety:
        if w is not None:
            box.addWidget(w)
    nwgt.setLayout(box)
    return nwgt

def hwgt(widgety,marg=0):
    return lwgt(widgety,QHBoxLayout(),marg)

def vwgt(widgety,marg=0):
    return lwgt(widgety,QVBoxLayout(),marg)    

class UniPole(QWidget):
    
    class Builder(object):
        def __init__(self):
            self.parent, self.wka, self.wkb = None,None,None # wka, wkb - QComboBox
            self.tokr, self.tsym = [], []
            self.re = False
            self.wyk = None
            self.funZm = None
            
        def buduj(self):
            return UniPole(self)
    
    def __init__(self,builder):
        QWidget.__init__(self,builder.parent)
        mbox = QVBoxLayout()
        mbox.setSizeConstraint(QLayout.SetMinimumSize)
        mbox.setContentsMargins(5,5,5,5)
        self.setLayout(mbox)
        self._wyk = builder.wyk
        self._funZmiana = builder.funZm # funkcja wywolywana w chwili zmiany wartosci
        self._ka, self._kb = builder.wka, builder.wkb
        self._tsym = builder.tsym
        self._ka.addItems(builder.tokr)
        self._ka.activated.connect(partial(self._kategorie, km='koda'))
        mbox.addWidget(self._ka)
        if self._kb is not None:
            self._kb.addItems(builder.tokr)
            self._kb.activated.connect(partial(self._kategorie,km='kodb'))
            mbox.addWidget(self._kb)
        else: # przypadek pola do edycji funkcji
            mbox.addWidget(QLabel())
        self._re = None
        if builder.re: # lista do okreslania relacji miedzy funkcjami
            self._re = QComboBox()
            self._re.addItems(['',u'-',u'/'])
        self._pew = QLineEdit()
        self._pew.editingFinished.connect(self._pewzm)
        mbox.addWidget(hwgt([self._re,self._pew]))
    
    def setDane(self,mapa):
        self._mapa = mapa
        self.wka = mapa.get('koda')
        self.wkb = mapa.get('kodb')
        self.wre = mapa.get('re','')
        self.wpew = mapa.get('pew','1')
        if self.wka is not None:
            self._ka.setCurrentIndex(self._tsym.index(self.wka[0]))
        else:
            self._ka.setCurrentIndex(0)
        if self.wkb is not None and self._kb is not None:
            bi = self._tsym.index(self.wkb[0])
            self._kb.setCurrentIndex(bi)
        elif self._kb is not None:
            self._kb.setCurrentIndex(0)
        if self._re is not None:
            self._re.setCurrentIndex(['','Z','P'].index(self.wre))
            self._re.activated.connect(self._rezm)
        self._pew.setText(str(self.wpew))
    
    def _rezm(self,i):
        tv = ['','Z','P']
        self._mapa['re'] = tv[i]
        self._zmianaDanych()
    
    def _pewzm(self):
        try:
            self._mapa['pew'] = float(str(self._pew.text()).replace(',','.'))
            self._zmianaDanych()
        except:
            pass
    
    def _kategorie(self,i,km=None):
        if 0 < i < len(self._tsym):
            menu = QComboBox(self._ka)
            ci = 0
            listaKat = self._wyk.listaKat(self._tsym[i])
            for (ki,k) in enumerate(listaKat):
                menu.addItem(k[1],k[0])
                if km is not None and k[0] == self._mapa.get(km):
                    ci = ki
            menu.setCurrentIndex(ci)
            menu.activated.connect(partial(self._cbwyb,menu=menu,klucz=km))
            menu.view().setTextElideMode(Qt.ElideNone)
            menu.setSizeAdjustPolicy(QComboBox.AdjustToContents)
            menu.showPopup()
        elif i == 0:
            self._mapa[km] = None
            self._zmianaDanych()
    
    def _zmianaDanych(self):
        if self._funZmiana is not None:
            self._funZmiana(self._mapa)
        
    def _cbwyb(self,i,menu=None,klucz=None):
        self._mapa[klucz] = str(menu.itemData(i).toString())
        if self._mapa[klucz] == '':
            self._mapa[klucz] = None
        self._zmianaDanych()

def _edPole(wyk,f,parent,tokr,tsym):
    b = UniPole.Builder()
    b.parent = parent
    b.wka, b.wkb = QComboBox(), QComboBox()
    b.tokr, b.tsym = tokr, tsym
    b.re = True
    b.wyk = wyk
    b.funZm = f
    return b.buduj()

def okrPole(wyk,f,parent):
    tokr = ['',u'EP. KAM.', u'EP. BRĄZU', u'EP.ŻELAZA', u'ŚREDN.', u'NOWOŻYT',u'WSPÓŁCZES.',u'PRADZIEJE']
    tsym = ['','K','B','Z','S','N','W','P'] 
    return _edPole(wyk,f,parent,tokr,tsym)
    
def jedPole(wyk,f,parent):
    tokr = ['',u'PALEO.',u'MEZO.','MEZ./NEOL.','NEO.', u'EP. BRĄZU', u'EP.ŻELAZA','WIELOKUL.']
    tsym = ['','P','M','L','N','B','Z','W']         
    return _edPole(wyk,f,parent,tokr,tsym)
    
def funPole(wyk,f,parent):
    b = UniPole.Builder()
    b.parent = parent
    b.wka = QComboBox()
    b.tokr = ['',u'OBRONNA',u'OBRZĘD.',u'OSAD.',u'SEPULKR.',u'GOSP.',u'KOMP. OS.',u'KOPIEC',u'POLE BITWY',u'SKARB', u'STAN.',u'REDEP.',u'WAŁY',u'LUŹNE'  ]
    b.tsym = ['','O','B','M','S','G','K','P','T','R','A','D','W','L']
    b.wyk = wyk
    b.funZm = f
    return b.buduj()

class FaktyWidok(QWidget):
    
    def __init__(self,st,con,parent=None):
        QWidget.__init__(self,parent)
        wlay = QVBoxLayout()
        self.setLayout(wlay)
        self._tab = QTableView()
        self._tab.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        owyk,jwyk,fwyk = okrWykaz(con), jedWykaz(con), funWykaz(con)
        self._fk = WykazFaktow(st,con,owyk,jwyk,fwyk)
        self._con = con
        self._model = ListaFaktow(self._fk)
        self._tab.setModel(self._model)
        wlay.addWidget(self._tab)
        self._op = okrPole(owyk,self._okrZmiana,self) # pole do edycji wykresow
        self._jp = jedPole(jwyk,self._jedZmiana,self)
        self._fp = funPole(fwyk,self._funZmiana,self)
        self._mp, self._wp = QLineEdit(), QLineEdit()
        self._btnUsu, self._btnZm = QPushButton(u'Usuń'), QPushButton(u'Dodaj')
        self._mp.editingFinished.connect(self._masZmiana)
        self._wp.editingFinished.connect(self._wyZmiana)
        self._btnZm.clicked.connect(self._zmienFk)
        self._btnUsu.clicked.connect(self._usunFk)
        wlay.addWidget(hwgt([self._op,self._jp,self._fp,vwgt([self._mp,self._btnUsu]),vwgt([self._wp,self._btnZm])]))
        self._tab.selectionModel().currentRowChanged.connect(self._zmBiezWier)

    def _zmienFk(self,b=True):
        self._model.beginResetModel()
        self._fk.zmien(self._bw)
        self._model.endResetModel()        
    
    def _usunFk(self,b=True):
        odp = QMessageBox.question(self,'Usuwanie',u'Czy na pewno chcesz usunąć fakt nr '+str(self._bw),QMessageBox.Yes | QMessageBox.No)
        if odp != QMessageBox.Yes:
            return
        self._model.beginResetModel()
        self._fk.usun(self._bw)
        self._model.endResetModel()  
        
    def _okrZmiana(self,dane):
        self._model.beginResetModel()
        r = self._bw
        self._fk.setMapa(r,{'okresa':dane['koda'],'okresb':dane['kodb'],
                             'okr_pewnosc':dane['pew'],'okr_relacja':dane['re']})
        self._model.endResetModel()

    def _jedZmiana(self,dane):
        self._model.beginResetModel()
        r = self._bw
        self._fk.setMapa(r,{'jeda':dane['koda'],'jedb':dane['kodb'],
                             'jed_pewnosc':dane['pew'],'jed_relacja':dane['re']})
        self._model.endResetModel()
        
    def _funZmiana(self,dane):
        self._model.beginResetModel()
        r = self._bw
        self._fk.setMapa(r,{'funkcja':dane['koda'],'fun_pewnosc':dane['pew']})
        self._model.endResetModel()
    
    def _masZmiana(self):
        self._model.beginResetModel()
        self._fk.setWartosc(self._bw,'masowy',unicode(self._mp.text()))
        self._model.endResetModel()
    
    def _wyZmiana(self):
        self._model.beginResetModel()
        self._fk.setWartosc(self._bw,'wydzielony',unicode(self._wp.text()))
        self._model.endResetModel()
    
    def _zmBiezWier(self, p, b):
        self._bw = p.row()
        self._op.setDane({'koda':self._fk.get(self._bw,'okresa'),'kodb':self._fk.get(self._bw,'okresb'),'pew':self._fk.get(self._bw,'okr_pewnosc','1'),'re':self._fk.get(self._bw,'okr_relacja','')})
        self._jp.setDane({'koda':self._fk.get(self._bw,'jeda'),'kodb':self._fk.get(self._bw,'jedb'),'pew':self._fk.get(self._bw,'jed_pewnosc','1'),'re':self._fk.get(self._bw,'jed_relacja','')})
        self._fp.setDane({'koda':self._fk.get(self._bw,'funkcja'),'pew':self._fk.get(self._bw,'fun_pewnosc','1')})
        self._mp.setText(self._fk.get(self._bw,'masowy',''))
        self._wp.setText(self._fk.get(self._bw,'wydzielony',''))
        
    def zatwierdz(self):
        if self._con is None:
            return
        self._con.zatwierdz()
        self._con.zakoncz()
        self._con = None
        
    def wycofaj(self):
        if self._con is None:
            return
        self._con.wycofaj()
        self._con.zakoncz()
        self._con = None
