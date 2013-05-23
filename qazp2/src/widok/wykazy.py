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

from PyQt4.QtGui import QFrame, QTableView, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox,QLineEdit, QMessageBox, QAction
from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant, SIGNAL, QObject
from dane.zrodla import Wykaz, get_warstwa, getPolaczenie2

class WykModel(QAbstractTableModel):
    
    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self,parent)
        self._wyk = []
        self._wybrany = None
        
    def setWykaz(self, wykaz):
        self._wyk = wykaz
    
    def endResetModel(self):
        self._wybrany = None
        QAbstractTableModel.endResetModel(self)
        
    def ident(self):
        if self._wybrany is None:
            return -1
        return self._wybrany[0].toInt()[0]
    
    def ostatni(self):
        return (self._wybrany[0].toInt()[0],unicode(self._wybrany[1].toString()))    
        
    def rowCount(self, *args, **kwargs):
        return len(self._wyk)
    
    def columnCount(self, *args, **kwargs):
        return 1
    
    def data(self, indeks, rola = Qt.DisplayRole):
        if rola == Qt.DisplayRole and indeks.column() == 0 and indeks.row() < len(self._wyk):
            self._wybrany = self._wyk[indeks.row()]
            return self._wybrany[1]
        return QVariant()
        
    def headerData(self, sekcja, orientacja, rola = Qt.DisplayRole):
        if orientacja == Qt.Vertical:
            return None
        if sekcja > 0:
            raise Exception("headerData: indeks %d poza zakresem [0,%d]"%(sekcja,len(self._nag)-1))
        if rola == Qt.DisplayRole:
            if sekcja == 0:
                return u'Nazwa'
            else:
                return None

def listaStart(con,nazwa):
    sql = 'select distinct start from '+nazwa+' order by start'
    rt = []
    for w in con.wszystkie(sql):
        rt.append(QVariant(w[0]).toString())
    return rt
                
class WykDialog(QFrame):
    
    def __init__(self, con, nazwa, win, parent=None):
        QFrame.__init__(self,parent)
        self._con = con
        self._nazWyk = nazwa
        self._win = win
        self._wyk = Wykaz(con,nazwa)
        self.vbox = QVBoxLayout(self)
        self._tab = QTableView(self)
        self._mwyk = WykModel(self)
        self._mwyk.setWykaz(self._wyk)
        self._tab.setModel(self._mwyk)
        self.vbox.addWidget(self._tab)
        edwgt = QWidget()
        hed = QHBoxLayout()
        edwgt.setLayout(hed)
        self._cbstart = QComboBox(edwgt)
        try:
            self._skroty = listaStart(self._con, self._nazWyk)
        except:
            stmt = self._con.prep('update miejscowosci set start=? where id = ?' )
            stmt.wykonaj(['BE', 23])
            stmt.wykonaj(['ZL', 7])
            self._con.zatwierdz()
            self._skroty = listaStart(self._con, self._nazWyk)
        self._cbstart.addItems(self._skroty)
        hed.addWidget(self._cbstart)
        self._cbstart.currentIndexChanged.connect(self._zmWyk)
        self._edtxt = QLineEdit(edwgt)
        hed.addWidget(self._edtxt)
        btnUsu = QPushButton(u'Usuń')
        btnUsu.clicked.connect(self._usunZaz)
        hed.addWidget(btnUsu)
        btnDod = QPushButton(u'Dodaj')
        btnDod.clicked.connect(self._dodajNowy)
        hed.addWidget(btnDod)
        btnZm = QPushButton(u'Zmień')
        btnZm.clicked.connect(self._zmianaNaz)
        hed.addWidget(btnZm)
        btnEx = QPushButton(u'Zamknij')
        btnEx.clicked.connect(self._zamknij)
        hed.addWidget(btnEx)
        self.vbox.addWidget(edwgt)
        if len(self._skroty) > 0:
            self._cbstart.setCurrentIndex(1);
        self._tab.selectionModel().currentRowChanged.connect(self._zmBiezWier)
    
    def _zamknij(self,arg):
        self._win.usun(self)
        
    def _zmWyk(self,et):
        self._mwyk.beginResetModel()
        self._wyk.wypelnij(unicode(self._cbstart.currentText()))
        self._mwyk.endResetModel()
        self._edtxt.setText('')
        
    def _zmBiezWier(self,biez,poprz):
        self._edtxt.setText(biez.data().toString())
    
    def _zmianaNaz(self,arg):
        sm = self._tab.selectionModel()
        indeks = sm.currentIndex()
        if indeks.isValid():
            n = self._wyk[indeks.row()]
            wid = n[0].toInt()[0]
            wn = unicode(n[1].toString())
        else:
            return
        if not sm.hasSelection() :
            QMessageBox.information(self,'Zmiana',u'Proszę wybrać nazwę do zmiany')
            return
        odp = QMessageBox.question(self,'Zmiana',u'Czy na pewno chcesz zmienić nazwę '+wn+' na '+self._edtxt.text()+' ?',QMessageBox.Yes | QMessageBox.No)
        if odp != QMessageBox.Yes:
            return
        if self._wyk.zmien(wid,unicode(self._edtxt.text())):
            self._mwyk.beginResetModel()
            self._wyk.wypelnij()
            self._mwyk.endResetModel()
            self._tab.selectionModel().clearSelection()
        else:
            QMessageBox.warning(self,'Zmiana',u'Podana nazwa już znajduje się w wykazie')
    
    def _dodajNowy(self,arg):
        odp = QMessageBox.question(self,'Dodawanie',u'Czy na pewno chcesz dodać nazwę '+self._edtxt.text()+' ?',QMessageBox.Yes | QMessageBox.No)
        if odp != QMessageBox.Yes:
            return
        if self._wyk.dodaj(unicode(self._edtxt.text())):
            self._mwyk.beginResetModel()
            self._wyk.wypelnij()
            self._mwyk.endResetModel()
            self._tab.selectionModel().clearSelection()
        else:
            QMessageBox.warning(self,'Dodawanie',u'Podana nazwa już znajduje się w wykazie')
        
    def _usunZaz(self,arg):
        sm = self._tab.selectionModel()
        indeks = sm.currentIndex()
        if indeks.isValid():
            n = self._wyk[indeks.row()]
            wid = n[0].toInt()[0]
        else:
            return
        if not sm.hasSelection() :
            QMessageBox.information(self,'Usuwanie',u'Proszę wybrać nazwę do usunięcia')
            return
        odp = QMessageBox.question(self,'Usuwanie',u'Czy na pewno chcesz usunąć nazwę '+self._edtxt.text()+' ?',QMessageBox.Yes | QMessageBox.No)
        if odp != QMessageBox.Yes:
            return
        self._wyk.usun(wid)
        self._mwyk.beginResetModel()
        self._wyk.wypelnij()
        self._mwyk.endResetModel()
        self._tab.selectionModel().clearSelection()

class WykazAkcja(QAction):
    
    def __init__(self,et,nazwa,iface,window):
        QAction.__init__(self,et,window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        self._naz = nazwa
        
    def wykonaj(self):
        st = get_warstwa('stanowiska')
        if st is None:
            QMessageBox.warning(self._win,u'Wykazy',u'Wykazy wymagają otwartej warstwy "stanowiska"')
            return 
        self._win.dodaj(WykDialog(getPolaczenie2(st),self._naz,self._win))

class FkWykazAkcja(QAction):
    def __init__(self,et,nazwa,iface,window):
        QAction.__init__(self,et,window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        self._naz = nazwa
        
    def wykonaj(self):
        st = get_warstwa('stanowiska')
        if st is None:
            QMessageBox.warning(self._win,u'Wykazy',u'Wykazy wymagają otwartej warstwy "stanowiska"')
            return 
        else:
            con = getPolaczenie2(st)
            con.jeden('select count(*) from '+self._naz)
        #self._win.dodaj(WykDialog(getPolaczenie2(st),self._naz,self._win))
        