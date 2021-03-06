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

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from dane.tabela import *


class Filtr(object):

    def __init__(self, tn, te, an, ae, ww, we=None):
        fmt = u'%s.%s = %s'
        if we is None:
            self._uc = fmt % (te, ae, ww)
        else:
            self._uc = fmt % (te, ae, we)
        self._tnazwa, self._anazwa, self._wartosc = tn, an, ww
    
    def __str__(self):
        return self._uc
    
    @property    
    def tabela(self):
        return self._tnazwa
    
    @property
    def atrybut(self):
        return self._anazwa
    
    @property
    def wartosc(self):
        return self._wartosc

class Filtr2(object):

    def __init__(self, atr, wartosc, rep=None):
        fmt = u'%s.%s = %s'
        if rep is None:
            self._widok = fmt % (atr.tabela.tetykieta, atr.aetykieta, wartosc)
        else:
            self._widok = fmt % (atr.tabela.tetykieta, atr.aetykieta, rep)
        self._atr = atr
        self._war = wartosc

    def __str__(self):
        return self._widok

    @property
    def tabela(self):
        return self._atr.tabela

    @property
    def atrybut(self):
        return self._atr

    @property    
    def wartosc(self):
        return self._war
        
class ListaModel(QAbstractListModel):

    def __init__(self, filtry, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._filtry = filtry
        
    def rowCount(self, parent=QModelIndex()):
        return len(self._filtry)
        
    def data(self, indeks, rola=Qt.DisplayRole):
        if rola == Qt.DisplayRole:
            return str(self._filtry[indeks.row()])
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role==Qt.DisplayRole and section==0 and orientation==Qt.Vertical:
            return u'Filtry'

class ComboTxt(QWidget):
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        box = QHBoxLayout(self)
        self.setLayout(box)
        self._cb = QComboBox()
        self._cb.setMinimumWidth(200)
        self._txt = QLineEdit()
        self._txt.setMinimumWidth(200)
        self._txt.setVisible(False)
        box.addWidget(self._cb)
        box.addWidget(self._txt)
        
    def lista(self, tab):
        self._cb.clear()
        self._cb.addItems(tab)
        self._cb.setVisible(True)
        self._txt.setVisible(False)
        
    def tekst(self):
        self._txt.setVisible(True)
        self._cb.setVisible(False)
    
    @property    
    def wartosc(self):
        if self._txt.isVisible():
            return str(self._txt.text())
        elif self._cb.isVisible():
            return self._cb.currentIndex()
        return None

class Formularz(QWidget):

    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._tabele = []
        self._twyb, self._awyb = -1, -1        
    
    def dodajTabele(self, t):
        self._tabele.append(t)
    
    def _initWar(self, atr):
        if atr.dozwolone is None:
            self._warCt.tekst()
        else:
            self._warCt.lista(atr.dozwolone)
    
    def _initAtr(self, ti):
        self._atrCb.clear()
        self._atrCb.addItems([a.aetykieta for a in self._tabele[ti].atrs])
        self._awyb = 0
        self._initWar(self._tabele[ti].atrs[0])
    
    def _wybierzTab(self, i):
        if i != self._twyb:
            self._twyb = i
            self._initAtr(i)            
    
    def wyswietl(self):
        form = QFormLayout(self)
        self.setLayout(form)
        self._tabCb, self._atrCb = QComboBox(), QComboBox()
        self._warCt = ComboTxt()
        form.addRow('Tabela', self._tabCb)
        form.addRow('Atrybut', self._atrCb)
        form.addRow(u'Wartość', self._warCt)
        if self._tabele:
            self._tabCb.addItems([t.tetykieta for t in self._tabele])
            self._wybierzTab(0)
        self._tabCb.activated.connect(self._wybierzTab)
        self._atrCb.activated.connect(self._zmienAtr)
    
    def _zmienAtr(self, i):
        self._awyb = i
        self._initWar(self._tabele[self._twyb].atrs[i])
        
    def wybrane(self):
        return (self._twyb, self._awyb, self._warCt.wartosc)

class Edytor(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        box = QVBoxLayout(self)
        self.setLayout(box)
        self.form = Formularz()
        box.addWidget(self.form, Qt.AlignTop)
        dodajBtn = QPushButton(u'Dodaj')
        usunBtn = QPushButton(u'Usuń')
        bb = QDialogButtonBox()
        bb.addButton(dodajBtn, QDialogButtonBox.AcceptRole)
        bb.addButton(usunBtn, QDialogButtonBox.RejectRole)
        bb.accepted.connect(self._dodajKlik)
        bb.rejected.connect(self._usunKlik)
        box.addWidget(bb) 
        box.setSizeConstraint(QLayout.SetFixedSize)
    
    def dodajTabele(self, tab):
        self.form.dodajTabele(tab)
    
    def wyswietl(self):
        self.form.wyswietl()
        
    def _dodajKlik(self):
        self.dodanie.emit(self.form.wybrane())

    def _usunKlik(self):
        self.usuniecie.emit()

    dodanie = pyqtSignal(tuple, name='dodanie')
    
    usuniecie = pyqtSignal(name='usuniecie')


class FiltrWidget(QWidget):
    
    def __init__(self, con, tabele, parent=None):
        QWidget.__init__(self, parent)
        self._filtry = []
        self._tabele = []
        hwgt = QWidget(self)
        hbox = QHBoxLayout(hwgt)
        hwgt.setLayout(hbox)
        vbox = QVBoxLayout(self)
        self.setLayout(vbox)
        self._widok = QListView()
        self._wmodel = ListaModel(self._filtry, self._widok)
        self._widok.setModel(self._wmodel)
        hbox.addWidget(self._widok)
        ed = Edytor()
        self._tabele.extend(tabele)
        for t in self._tabele:
            ed.dodajTabele(t)
        hbox.addWidget(ed)
        ed.dodanie.connect(self._nowyFiltr)
        ed.usuniecie.connect(self._usunFiltr)
        ed.wyswietl()
        
        vbox.addWidget(hwgt)
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        vbox.addWidget(bb)
        bb.accepted.connect(self._zatwierdz)
        bb.rejected.connect(self._anuluj)


        
    def _nowyFiltr(self, wyb):
        t = self._tabele[wyb[0]]#.tetykieta
        a = t.atrs[wyb[1]]
        war = wyb[2]
        rep = None
        if isinstance(war, int):
            rep = a.etwar(war)
            war = a.kodwar(war)
        self._wmodel.beginResetModel()
        self._filtry.append(Filtr2(a, war, rep))
        self._wmodel.endResetModel()
    
    filtruj = pyqtSignal(dict, name='filtruj')
    
    anuluj = pyqtSignal(name='anuluj')
    
    def _anuluj(self):
        self.anuluj.emit()
        
    def _zatwierdz(self):
        df = {}
        for f in self._filtry:
            if f.tabela not in df:
                df[f.tabela] = {}
            dt = df[f.tabela]
            if f.atrybut not in dt:
                dt[f.atrybut] = []
            df[f.tabela][f.atrybut].append(f.wartosc)
        self.filtruj.emit(df)
        
    def _usunFiltr(self):
        i = self._widok.selectionModel().currentIndex().row()
        if i < 0 or i >= len(self._filtry):
            return
        self._wmodel.beginResetModel()
        self._filtry.pop(i)
        self._wmodel.endResetModel()