'''
Created on Jul 24, 2011

@author: milosz
'''

from PyQt4.QtGui import QDialog, QVBoxLayout,QTableWidget, QAbstractItemView,QFileDialog
from PyQt4.QtGui import QDialogButtonBox,QTableWidgetItem,QApplication,QStatusBar,QPrinter
from PyQt4.QtCore import SIGNAL
from lib.dokument import Dokument

class ZestWidok(QDialog):

    def __init__(self,zest,parent=None):
        QDialog.__init__(self,parent)
        self.resize(430,347)
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.initTab()
        self.wypelnijTab(zest)
        self.zest = zest
        
    def initTab(self):
        self.tabela = QTableWidget(self)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela.setSortingEnabled(False)
        self.vbox.addWidget(self.tabela)
        self.btns = QDialogButtonBox(self)
        self.btns.setStandardButtons(QDialogButtonBox.Close | QDialogButtonBox.Save)
        self.vbox.addWidget(self.btns)
        self.status = QStatusBar(self)
        self.vbox.addWidget(self.status)
        self.connect(self.btns,SIGNAL('rejected()'),self.zamknij)
        self.connect(self.btns,SIGNAL('accepted()'),self.zapisz_pdf)
        self.connect(self, SIGNAL('close()'),self.zamknij)
        
    def __item(self,var):
        if isinstance(var,unicode):
            return QTableWidgetItem(var)
        else:
            return QTableWidgetItem(QApplication.translate(unicode(var).encode('utf-8'), unicode(var).encode('utf-8'), None,QApplication.UnicodeUTF8)) 
    
    def wypelnijTab(self,zest):
        #zest.wykonaj()
        zestpola = zest.nazwy_pol()
        self.tabela.setColumnCount(len(zestpola))
        #self.tabela.setVerticalHeaderLabels(zestpola)
        self.heads = []
        for (zi,z) in enumerate(zestpola):
            self.tabela.setHorizontalHeaderItem(zi,self.__item(z.upper()))
            self.heads.append(unicode(self.tabela.horizontalHeaderItem(zi).text()))
        wiersze_count = 0
        for wiersz in zest.wiersze():
            self.tabela.insertRow(wiersze_count)
            for (pi,pole) in enumerate(wiersz):
                self.tabela.setItem(wiersze_count,pi,self.__item(pole))
            wiersze_count += 1
        self.tabela.setSortingEnabled(True)
        self.tabela.resizeColumnsToContents()   
        #self.status.showMessage('Znaleziono: %s'%str(wiersze_count)) 
        
    def zapisz_pdf(self):
        rc = self.tabela.rowCount()
        cc = self.tabela.columnCount()
        #head = []
        #for c in range(0,cc):
        #    print self.tabela.horizontalHeaderItem(cc)
        #    head.append(unicode(self.tabela.horizontalHeaderItem(cc).text()))
        wiersze = []
        for r in range(0,rc):
            w = []
            for c in range(0,cc):
                w.append(unicode(self.tabela.item(r,c).text()))
            wiersze.append(w)
        nazwa = QFileDialog.getSaveFileName(self)
        dok = Dokument()
        dok.dodaj_tabele(self.heads, wiersze)
        dok.zapisz_pdf(nazwa)
        print 'zapis ok'
    
    def zamknij(self):
        self.done(0)        