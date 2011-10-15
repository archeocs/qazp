from PyQt4.QtCore import *
from PyQt4.QtGui import * 

class EdytorWgt(QWidget):

    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.hbox = QHBoxLayout()
        self.setLayout(self.hbox)
    
    def dodaj_widget(self,widget,prefsz=0,prefwy=0):
        self.hbox.addWidget(widget)
        #else:
        #    self.grid.addWidget(widget,r,c)
        if prefsz > 0:
            widget.setMinimumWidth(prefsz)
            widget.setMaximumWidth(prefsz)
        if prefwy > 0:
            widget.setMinimuHeight(prefwy)
            widget.setMaximumHeight(prefwy)
        return widget
        

class TabelaTab(QWidget):
    
    zaznaczony = -1 # zaznaczony wiersz
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.initTab(parent)
        
    def initTab(self,parent=None):
        self.tabela = QTableWidget(parent)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.setSelectionMode(QAbstractItemView.SingleSelection)
        self.vbox.addWidget(self.tabela)    
        self.pasek = self.initPasek(parent)
        self.vbox.addWidget(self.pasek)
        self.tabela.setSortingEnabled(False)
        self.tabela.setRowCount(1)
        self.tabela.setItem(0,0,self.__item('<Nowy>'))
        self.tabela.setColumnCount(6)
        self.connect(self.tabela,SIGNAL('currentCellChanged (int,int,int,int)'),self.wiersz_klik)
        
    def __item(self,var):
        #print var
        #x = QApplication.translate(str(var), str(var), None,QApplication.UnicodeUTF8)
        if isinstance(var,unicode):
            return QTableWidgetItem(var)
        else:
            return QTableWidgetItem(QApplication.translate(unicode(var).encode('utf-8'), unicode(var).encode('utf-8'), None,QApplication.UnicodeUTF8))     
        
    def dodajWiersz(self,nowy_wiersz):
        tr = self.tabela.rowCount()
        for (wi,w) in enumerate(nowy_wiersz):
            #print w
            self.tabela.setItem(tr-1,wi,self.__item(w))
        self.tabela.insertRow(tr)    
        self.tabela.setItem(tr,0,self.__item('<Nowy>'))   
        self.tabela.resizeColumnsToContents()   
    
    def zmienWiersz(self,tab_ind,wiersz):
        for (wi,w) in enumerate(wiersz):
            self.tabela.setItem(tab_ind,wi,self.__item(w))
        self.tabela.resizeColumnsToContents()
        
    def zatwierdzZmiany(self,i,nowy):
        pass  
    
    
    def dodajPola(self,pasek):
        pass
        
    def wiersz_klik(self,akt_wier,akt_kol,poprz_wier,poprz_kol):
        if akt_wier != self.zaznaczony:
            self.zaznaczony = akt_wier
            if akt_wier < self.tabela.rowCount()-1:
                tb = []
                for kol_num in range(self.tabela.columnCount()):
                    tb.append(self.tabela.item(akt_wier,kol_num))
                self.aktywuj_edytor(akt_wier,tb) # klikniecie wiersza z danymi
            else:
                self.aktywuj_edytor(akt_wier,None) #  klikniecie wiersza <Nowy>
            
    
    def aktywuj_edytor(self,indeks,wartosci):
        pass
    
    def zapisz_click(self):
        self.zatwierdzZmiany(self.zaznaczony,nowy=(self.zaznaczony == self.tabela.rowCount()-1))
    
    def initPasek(self,parent=None):
        pasek = EdytorWgt(parent)
        #self.vbox.addWidget(pasek)
        self.dodajPola(pasek)
        self.zapisz_btn = pasek.dodaj_widget(QPushButton('Zapisz'),prefsz=50)
        self.connect(self.zapisz_btn,SIGNAL('clicked()'),self.zapisz_click)
        self.usun_btn = pasek.dodaj_widget(QPushButton('Usun'),prefsz=50)    
        return pasek