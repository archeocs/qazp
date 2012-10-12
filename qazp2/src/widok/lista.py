'''
Created on Sep 9, 2012

@author: milosz
'''

from PyQt4.QtGui import QFrame, QVBoxLayout,QTableView,QGroupBox,QHBoxLayout,QPushButton,QButtonGroup,QStyledItemDelegate,QTableWidget
from PyQt4.QtCore import QAbstractTableModel, QVariant, SIGNAL
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
            #print self._nag[sekcja], sekcja
            return QVariant(self._nag[sekcja])
        
class GTabModel2(QAbstractTableModel):
    
    def __init__(self,nag,dane=[],parent=None): # nag = [(Naglowek,klucz),...]
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
            v = self._dane[r][self._nag[c][1]]
            #v = self._dane[r].wartosc(c)
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
            #print self._nag[sekcja], sekcja
            return QVariant(self._nag[sekcja][0])

class GFrame(QFrame):
    
    def __init__(self,win,gobs=[],parent=None):
        QFrame.__init__(self,parent)
        self._gobs = gobs
        self.init_frame()
        self._win = win
        
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
        btn_ok = QPushButton('OK')
        btn_ok.setObjectName('btn_ok')
        btn_zmien = QPushButton(u'Zmien')
        btn_zmien.setObjectName('btn_zmien')
        btn_anul = QPushButton('Anuluj')
        btn_anul.setObjectName('btn_anul')
        btn_wysw = QPushButton('Wyswietl')
        btn_wysw.setObjectName('btn_wysw')
        btn_usun = QPushButton('Usun')
        btn_usun.setObjectName('btn_usun')
        hbox.addWidget(btn_ok)
        hbox.addWidget(btn_zmien)
        hbox.addWidget(btn_usun)
        hbox.addWidget(btn_wysw)
        hbox.addWidget(btn_anul)
        btn_box.setLayout(hbox)      
        vbox.addWidget(btn_box)
        
        grupa = QButtonGroup(btn_box)
        grupa.addButton(btn_ok,1)
        grupa.addButton(btn_anul,2) 
        grupa.addButton(btn_zmien,3)
        grupa.addButton(btn_wysw,4)
        grupa.addButton(btn_usun,5)
        self.connect(grupa, SIGNAL('buttonPressed(int)'), self.btn_klik)
        
    def wybrany_wiersz(self):
        ci = self._tab.currentIndex()
        return (ci,self._gobs[ci.row()])
        
    def btn_klik(self,id):
        if id == 1:
            self._akcjaOk()
        elif id == 2:
            self._akcjaAnul()
        elif id == 3:
            self.akcja_zmien()
        elif id == 4:
            self.akcja_wyswietl()
        elif id == 5:
            self.akcja_usun()
    def utworz_model(self,gobs):
        raise Exception("GFrame.utworz_model: brak implementacji") 
    
    # domyslne implementacje akcji (np ok, anuluj ...)
    
    def _akcjaOk(self):
        self._win.usun(self)
        
    def _akcjaAnul(self):
        self._win.usun(self)
        
    def akcja_zmien(self):
        print 'akcja_zmien: brak implementacji'
        
    def akcja_wyswietl(self):
        print 'akcja_zmien: brak implementacji'
        
    def akcja_usun(self):
        pass