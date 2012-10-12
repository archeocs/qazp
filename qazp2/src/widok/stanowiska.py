# -*- coding: utf-8 -*-

'''
Created on Oct 6, 2012

@author: milosz
'''
from PyQt4.QtCore import SIGNAL,QObject
from PyQt4.QtGui import QAction,QMessageBox,QInputDialog,QWidget
from widok.lista import GTabModel2, GFrame
from dane.zrodla import gstanowiska, get_warstwa, szukaj_stanowiska,getPolaczenie
from widok.sted import Edytor

def tab_model(obiekty,parent=None):
    return GTabModel2([('Ident','id'),('Obszar','obszar'),('Nr na obszarze','nr_obszar'),('Rodzaj','rodzaj_badan')
                      ,('Data','data'),('Autor','autor'),('Uwagi','uwagi')],obiekty,parent)
    
    
class StanowiskaFrame(GFrame):
    
    warstwa = None
    def __init__(self,warstwa,iface,win,parent=None):
        GFrame.__init__(self,win,gstanowiska(warstwa))
        self.setObjectName('stanowiska')
        self.warstwa = warstwa
        self._if = iface
        self._win = win
        self._win.statusBar().showMessage("Wyszukano %s obiektow %s"%(str(self.warstwa.featureCount()),
                                                                      self.warstwa.dataProvider().dataSourceUri()))
        
    def utworz_model(self, gobs):
        return tab_model(gobs, self)
    
    def akcja_zmien(self):
        ww = self.wybrany_wiersz()[1]
        ed = Edytor(self.warstwa,ww,self._win)
        self._win.dodaj(ed)

class WyszukajAkcja(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,'Wyszukaj',window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        trasy = get_warstwa('stanowiska')
        if trasy is None:
            QMessageBox.warning(self._win,u'Wyszukaj',u'Przed wyszukiwaniem należy otworzyć warstwę "stanowiska"')
            return 
        warunek = QInputDialog.getText(self._win, 'Miejsca', 'Wprowadz warunek', text='id > 0')
        if warunek[1]:
            mf = StanowiskaFrame(szukaj_stanowiska(unicode(warunek[0])),self._iface,self._win)
            self._win.dodaj(mf)
            
class PolaczSql(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,u'Połączenie',window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        db = getPolaczenie(get_warstwa('stanowiska'))
        if db.isOpen():
            QMessageBox.information(self, u'Połączenie', 'Połączenie nawiązane')
        