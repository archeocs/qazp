# -*- coding: utf-8 -*-

#from PyQt4.QtCore import *
#from PyQt4.QtGui import * 
from PyQt4.QtGui import QComboBox, QLineEdit
from PyQt4.QtCore import SIGNAL, QString
from uniwersalne import StronaSiatka

# klasa konstruujaca zakladke z informacjami
class InfoTab(StronaSiatka):

    zmiany_slo = {}
    
    def __init__(self,ile_k,dane_src):
        StronaSiatka.__init__(self,ile_k)
        self.zmiany_slo = {}
        self.dane = dane_src
        
    #def dodaj_widget(self,widget,etykieta,ident=None):
    #    super.dodaj_widget(widget,etykieta)

    def dodaj_combo(self,etykieta,sel_ind,wartosci=['NIE','TAK'],nazwa=None):
        w = self.dodaj_widget(QComboBox(),etykieta)
        w.addItems(wartosci)
        #print sel_ind
        w.setCurrentIndex(sel_ind)
        if nazwa is not None:
            w.setObjectName(nazwa)
        self.connect(w,SIGNAL('currentIndexChanged(int)'),self.zmiana)
        return w
    
    def dodaj_txt(self,etykieta,wartosc=None,nazwa=None):
        w = self.dodaj_widget(QLineEdit(),etykieta)
        w.setText(wartosc)
        if nazwa is not None:
            w.setObjectName(nazwa)
        self.connect(w,SIGNAL('textEdited(const QString&)'),self.zmiana)
        return w
        
        
    def zmiana(self,i):
        #print i
        if isinstance(i,int):
            self.zmiany_slo[str(self.sender().objectName())] = i
        elif isinstance(i,QString):
            self.zmiany_slo[str(self.sender().objectName())] = unicode(i)
        
    def zapisz(self):
        for it in self.zmiany_slo.items():
            self.dane.zmien(it[0],it[1])
            #print it, hasattr(self.dane,it[0])
            #if hasattr(self.dane,it[0]):
            #    setattr(self.dane,it[0],it[1])   
        self.dane.zapisz()
        
