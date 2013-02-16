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

from PyQt4.QtGui import QFrame, QVBoxLayout,QTableView,QGroupBox,QHBoxLayout,QPushButton,QButtonGroup,\
                        QStyledItemDelegate,QShortcut,QKeySequence
from PyQt4.QtCore import QAbstractTableModel, QVariant, SIGNAL, QModelIndex
from PyQt4.QtCore import Qt

class GTabModel(QAbstractTableModel):
    
    def __init__(self,nag,dane=[],parent=None):
        QAbstractTableModel.__init__(self,parent)
        self._nag = nag
        self._dane = dane
        
    def rowCount(self, *args, **kwargs):
        return len(self._dane)
    
    def columnCount(self, *args, **kwargs):
        return len(self._nag)
    
    def data(self, indeks, rola = Qt.DisplayRole):
        if rola == Qt.DisplayRole:
            r,c = indeks.row(), indeks.column()
            v = self._dane[r].wartosc(c)
            if not isinstance(v, QVariant):
                return QVariant(self._dane[r].wartosc(c)).toString()
            else:
                return v.toString()
        else:
            return QVariant()
    
    def headerData(self, sekcja, orientacja, rola = Qt.DisplayRole):
        if orientacja == Qt.Vertical:
            return None
        if sekcja < 0 or sekcja >= len(self._nag):
            raise Exception("headerData: indeks %d poza zakresem [0,%d]"%(sekcja,len(self._nag)-1))
        if rola == Qt.DisplayRole:
            return QVariant(self._nag[sekcja])
                
class GTabModel2(QAbstractTableModel):
    
    def __init__(self,nag,dane=[],parent=None): # nag = [(Naglowek,klucz),...]
        QAbstractTableModel.__init__(self,parent)
        self._nag = nag
        self._origDane = dane
        self._dane = []
        self._dane.extend(dane)
        
    def rowCount(self, *args, **kwargs):
        return len(self._dane)
    
    def columnCount(self, *args, **kwargs):
        return len(self._nag)
    
    def data(self, indeks, rola = Qt.DisplayRole):
        if rola == Qt.DisplayRole:
            r,c = indeks.row(), indeks.column()
            v = self._dane[r][self._nag[c][1]]
            if not isinstance(v, QVariant):
                return QVariant(v).toString()
            else:
                return v.toString()
        else:
            return QVariant()
    
    def headerData(self, sekcja, orientacja, rola = Qt.DisplayRole):
        if orientacja == Qt.Vertical:
            return None
        if sekcja < 0 or sekcja >= len(self._nag):
            raise Exception("headerData: indeks %d poza zakresem [0,%d]"%(sekcja,len(self._nag)-1))
        if rola == Qt.DisplayRole:
            return QVariant(self._nag[sekcja][0])
        
    def removeRows(self, row, count, parent=QModelIndex):
        ost = row+count-1
        if ost > len(self._dane)-1:
            ost = len(self._dane)-1
        self.beginRemoveRows(parent, row, ost)
        for x in range(ost-row+1):
            self._dane.pop(row)
        self.endRemoveRows()
        return True
    
    def setFiltr(self, daneFiltr):
        self.beginResetModel()
        self._dane = daneFiltr
        self.endResetModel()
    
    def usunFiltr(self):
        self.beginResetModel()
        self._dane = []
        self._dane.extend(self._origDane)
        self.endResetModel()
        return self._dane

class GFrame(QFrame):
    
    def __init__(self,win,gobs=[],parent=None):
        QFrame.__init__(self,parent)
        self._gobs = gobs
        self._win = win
        self.init_frame()
        
    def init_frame(self):
        vbox = QVBoxLayout(self)
        self._tab = QTableView(self)
        self._tab.setModel(self.utworz_model(self._gobs))
        self._tab.setItemDelegate(QStyledItemDelegate())
        vbox.addWidget(self._tab)
        self.setLayout(vbox)
        
        # przyciski
        
        btn_box = QGroupBox(self)
        hbox = QHBoxLayout(btn_box)
        btn_zamknij = QPushButton('Zamknij')
        btn_zamknij.setObjectName('btn_zamknij')
        btn_zmien = QPushButton(u'Edytuj (Ctrl+J)')
        btn_zmien.setObjectName('btn_zmien')
        btn_wysw = QPushButton('Wyswietl')
        btn_wysw.setObjectName('btn_wysw')
        btn_usun = QPushButton('Usun')
        btn_usun.setObjectName('btn_usun')
        btn_drukuj = QPushButton('Drukuj')
        btn_drukuj.setObjectName('btn_drukuj')
        btn_filtr = QPushButton('Filtruj')
        btn_filtr.setObjectName('btn_filtr')
        hbox.addWidget(btn_zamknij)
        hbox.addWidget(btn_zmien)
        hbox.addWidget(btn_usun)
        hbox.addWidget(btn_wysw)
        hbox.addWidget(btn_drukuj)
        hbox.addWidget(btn_filtr)
        btn_box.setLayout(hbox)      
        vbox.addWidget(btn_box)
        
        grupa = QButtonGroup(btn_box)
        grupa.addButton(btn_zamknij, 1)
        grupa.addButton(btn_zmien, 2)
        grupa.addButton(btn_wysw, 3)
        grupa.addButton(btn_usun, 4)
        grupa.addButton(btn_drukuj, 5)
        grupa.addButton(btn_filtr, 6)
        self.connect(grupa, SIGNAL('buttonPressed(int)'), self.btn_klik)
        QShortcut(QKeySequence(Qt.CTRL+Qt.Key_J),self._win).activated.connect(self.akcja_zmien)
    
    def getModel(self):
        return self._tab.model()    
        
    def wybrany_wiersz(self):
        ci = self._tab.currentIndex()
        self._wiersz = ci.row()
        return (ci,self._gobs[self._wiersz])
    
    def zmienWiersz(self,skok):
        self._wiersz+=skok
        if 0 <= self._wiersz < len(self._gobs):
            return self._gobs[self._wiersz]
        return None
    
    def wszystkie(self):
        return self._gobs
    
    def setFiltr(self, zbior):
        ng = []
        for g in self._gobs:
            ident = g['id']
            if isinstance(ident, QVariant):
                ident = ident.toInt()[0]
            if ident in zbior:
                ng.append(g)
        self._gobs = ng
        self.getModel().setFiltr(self._gobs) 
        return len(self._gobs)
        
    def btn_klik(self,id):
        if id == 1:
            self._akcjaOk()
        elif id == 2:
            self.akcja_zmien()
        elif id == 3:
            self.akcja_wyswietl()
        elif id == 4:
            self.akcja_usun()
        elif id == 5:
            self._akcjaDrukuj()
        elif id == 6:
            self._akcjaFiltruj()
    
    def utworz_model(self,gobs):
        raise Exception("GFrame.utworz_model: brak implementacji") 
    
    # domyslne implementacje akcji (np ok, anuluj ...)
    
    def _akcjaOk(self):
        self._win.usun(self)
        
    def _akcjaAnul(self):
        self._win.usun(self)
    
    def _akcjaDrukuj(self):
        pass
    
    def _akcjaFiltruj(self):
        pass
        
    def akcja_zmien(self):
        print 'akcja_zmien: brak implementacji'
        
    def akcja_wyswietl(self):
        print 'akcja_zmien: brak implementacji'
        
    def akcja_usun(self):
        pass