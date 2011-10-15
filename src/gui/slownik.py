# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import * 
from widgety.slow_dial import SlownikDialogDef as slow_dial
import uzytki

class SlownikDialog(QDialog,slow_dial):
    
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        
    def akcje(self):
        self.connect(self.dodaj_btn,SIGNAL('clicked()'),self.dodaj)
        self.connect(self.zmien_btn,SIGNAL('clicked()'),self.zmien)
        self.connect(self.usun_btn,SIGNAL('clicked()'),self.usun)
        self.connect(self.buttonBox,SIGNAL('accepted()'),self.zapisz)
        self.connect(self.buttonBox,SIGNAL('rejected()'),self.anuluj)
        self.connect(self.lista,SIGNAL('itemClicked(QListWidgetItem *)'),self.wybor)
        
    def dodaj(self):
        pass
        
    def usun(self):
        pass
        
    def zmien(self):
        pass
        
    def zapisz(self):
        pass
        
    def anuluj(self):
        pass
        
    def wybor(self,it):
        self.wybrany = it
        
    def wyb_txt(self):
        return unicode(self.wybrany.text())

#class LokalizacjaDialog(QDialog,lok_dial):
#    def __init__(self,parent=None):
#        QDialog.__init__(self,parent)
#        self.setupUi(self)
        
        
        
class AdminSlownik(SlownikDialog):
    def __init__(self,adm,tytul,parent=None):
        SlownikDialog.__init__(self,parent)
        self.akcje()
        self.admin = adm
        self.lista.clear()
        for m in self.admin.lista():
            self.lista.addItem(unicode(m))
        self.setWindowTitle(tytul)
            
    def dodaj(self):
        ret = QInputDialog.getText(self,'Nowy',uzytki.to_unicode('Wprowadź nową wartość'))
        print ret
        if ret[1]:
            nowy = self.admin.nowy(unicode(ret[0]))
            if nowy[1]:
                self.lista.addItem(unicode(nowy[0]))
            
    def zmien(self):
        ret = QInputDialog.getText(self,'Zmien',uzytki.to_unicode('Wprowadź nową wartość'),QLineEdit.Normal,uzytki.to_unicode(self.wyb_txt()))
        if ret[1]:
            zm = self.admin.zmien(self.wyb_txt(),unicode(ret[0]))
            if zm:
                self.lista.clear()
                for m in self.admin.lista(nowa=True):
                    self.lista.addItem(unicode(m))
                    
    def usun(self):
        us = self.admin.usun(self.wyb_txt())
        print us
        if us:
            self.lista.takeItem(self.lista.currentRow())
            
    def zapisz(self):
        self.admin.zapisz()
        self.done(1)
        
    def anuluj(self):
        self.done(0)

class KulturySlownik(AdminSlownik):
    def __init__(self,dazp,parent=None):
        AdminSlownik.__init__(self,dazp.kultury(),"Kultury",parent)
        
class EpokiSlownik(AdminSlownik):
    def __init__(self,dazp,parent=None):
        AdminSlownik.__init__(self,dazp.epoki(),"Epoki",parent)
        
class FunkcjeSlownik(AdminSlownik):
    def __init__(self,dazp,parent=None):
        AdminSlownik.__init__(self,dazp.funkcje(),"Funkcje",parent)            
        
class PowiatySlownik(AdminSlownik):
    def __init__(self,dazp,parent=None):
        AdminSlownik.__init__(self,dazp.powiaty(),"Powiaty",parent)
        
class WojewodSlownik(AdminSlownik):
    def __init__(self,dazp,parent=None):
        AdminSlownik.__init__(self,dazp.wojewod(),uzytki.to_unicode("Województwa"),parent)
        
class MiejscaSlownik(AdminSlownik):
    
    def __init__(self,dazp,parent=None):
        AdminSlownik.__init__(self,dazp.miasta(),uzytki.to_unicode("Miejscowości"),parent)
        
class GminySlownik(AdminSlownik):
    def __init__(self,dazp,parent=None):
        AdminSlownik.__init__(self,dazp.gminy(),"Gminy",parent)