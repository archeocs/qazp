'''
Created on Jul 24, 2011

@author: milosz
'''

from PyQt4.QtGui import QDialog, QVBoxLayout,QTableWidget, QAbstractItemView
from PyQt4.QtGui import QDialogButtonBox,QTableWidgetItem,QApplication
from PyQt4.QtCore import SIGNAL

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
        self.btns.setStandardButtons(QDialogButtonBox.Close)
        self.vbox.addWidget(self.btns)
        self.connect(self.btns,SIGNAL('rejected()'),self.zamknij)
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
        print zestpola
        #self.tabela.setVerticalHeaderLabels(zestpola)
        for (zi,z) in enumerate(zestpola):
            print self.tabela.setHorizontalHeaderItem(zi,self.__item(z.upper()))
        wiersze_count = 0
        for wiersz in zest.wiersze():
            self.tabela.insertRow(wiersze_count)
            for (pi,pole) in enumerate(wiersz):
                self.tabela.setItem(wiersze_count,pi,self.__item(pole))
            wiersze_count += 1
        self.tabela.setSortingEnabled(True)
        self.tabela.resizeColumnsToContents()    
            
    def zamknij(self):
        self.done(0)        