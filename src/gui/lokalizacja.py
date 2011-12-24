# -*- coding: utf-8 -*-

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialog
from widgety.lokal_dialog import LokalDialogDef as lok_dial
import re

class LokalizacjaDialog(QDialog,lok_dial):
    indeksy = {}
    def __init__(self,lokal,dane,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi2(self)
        self.lokal = lokal
        self.m_slo = dane.miasta()
        self.g_slo = dane.gminy()
        self.p_slo = dane.powiaty()
        self.w_slo = dane.wojewod()
        self.arkusz_ed.setText(self.lokal.arkusz)
        self.nrark_ed.setText(self.lokal.nr_ark)
        self.nrmiej_ed.setText(self.lokal.nr_miej)
        self.set_slownik(self.m_slo,self.miasto_cb,self.m_slo.nazwa_ind(self.lokal.miej_naz)+1)
        self.set_slownik(self.g_slo,self.gmina_cb,self.g_slo.nazwa_ind(self.lokal.gm_naz)+1)
        print 'pow naz',self.lokal.pow_naz,self.p_slo.nazwa_ind(self.lokal.pow_naz)
        self.set_slownik(self.p_slo,self.powiat_cb,self.p_slo.nazwa_ind(self.lokal.pow_naz)+1)
        self.set_slownik(self.w_slo,self.woj_cb,self.w_slo.nazwa_ind(self.lokal.woj_naz)+1)
        self.connect(self.buttonBox,SIGNAL('accepted()'),self.zapisz)
        self.connect(self.buttonBox,SIGNAL('rejected()'),self.anuluj)
        self.connect(self.btnZnajdz, SIGNAL('clicked()'),self.przypisz_lok)
        self.setWindowTitle("Lokalizacja2")
        self.dane = dane
        
    def set_slownik(self,slow,combo,sel=0):
        combo.addItem(u"Nieokreślony")
        combo.addItems(slow.lista())
        combo.setCurrentIndex(sel)
        #print combo.objectName()
        self.indeksy[str(combo.objectName())] = sel-1
          
        
    def przypisz_lok(self):
        if self.lokal.czy_nowa:
            ark_txt = unicode(self.arkusz_ed.text())
            nrark_txt = unicode(self.nrark_ed.text())
            if ark_txt is None or ark_txt == "" or nrark_txt is None or nrark_txt == "":
                return
            elif re.match(r'^[0-9]+\-[0-9]+$',ark_txt) is None:
                return
            elif re.match(r'^[0-9]+$',nrark_txt) is None:
                return
            tmp_lok = self.dane.znajdz_lokal(self.lokal.stan,ark_txt,nrark_txt)
            if tmp_lok is not None:
                self.lokal = tmp_lok
                self.nrmiej_ed.setText(self.lokal.nr_miej)
                self.set_slownik(self.m_slo,self.miasto_cb,self.m_slo.nazwa_ind(self.lokal.miej_naz)+1)
                self.set_slownik(self.g_slo,self.gmina_cb,self.g_slo.nazwa_ind(self.lokal.gm_naz)+1)
                self.set_slownik(self.p_slo,self.powiat_cb,self.p_slo.nazwa_ind(self.lokal.pow_naz)+1)
                self.set_slownik(self.w_slo,self.woj_cb,self.w_slo.nazwa_ind(self.lokal.woj_naz)+1)    
                self.lokal.czy_nowa=True
        else:
            return None
        
    def zapisz(self): 
        ark_txt = unicode(self.arkusz_ed.text())
        nrark_txt = unicode(self.nrark_ed.text())
        nrmiej_txt = unicode(self.nrmiej_ed.text())
        if ark_txt is None or ark_txt == "" or nrark_txt is None or nrark_txt == "" or nrmiej_txt is None or nrmiej_txt == "":
            return
        elif re.match(r'^[0-9]+\-[0-9]+$',ark_txt) is None:
            return
        elif re.match(r'^[0-9]+$',nrark_txt) is None:
            return
        if ark_txt != self.lokal.arkusz:
            self.lokal.arkusz = ark_txt
            self.lokal.czy_zm = True
        if nrark_txt != self.lokal.nr_ark:
            self.lokal.nr_ark = nrark_txt
            self.lokal.czy_zm = True
        if nrmiej_txt != self.lokal.nr_miej:
            self.lokal.nr_miej = nrmiej_txt
            self.lokal.czy_zm = True
        
        if self.miasto_cb.currentIndex() > 0:
            if self.miasto_cb.currentIndex()-1 != self.indeksy["miasto_cb"]:
                self.lokal.miej_id = self.m_slo.indeks_sid(self.miasto_cb.currentIndex()-1)
                self.lokal.miej_naz = self.m_slo.indeks_naz(self.miasto_cb.currentIndex()-1)
                self.lokal.czy_zm = True
        else:
            return
        if self.gmina_cb.currentIndex() > 0:
            if self.gmina_cb.currentIndex()-1 != self.indeksy["gmina_cb"]:
                self.lokal.gm_id = self.g_slo.indeks_sid(self.gmina_cb.currentIndex()-1)
                self.lokal.czy_zm=True
        else:
            return
        pc = self.powiat_cb.currentIndex()-1
        wc = self.woj_cb.currentIndex()-1
        if pc != self.indeksy["powiat_cb"] and pc >= 0:
            self.lokal.pow_id = self.p_slo.indeks_sid(pc)
            
            self.lokal.czy_zm=True
        elif pc == 0:
            print pc        
        if wc != self.indeksy["woj_cb"] and wc >= 0:
            self.lokal.woj_id = self.w_slo.indeks_sid(wc)
            self.lokal.czy_zm=True
        else:
            print wc  
        self.lokal.zapisz()
        self.done(1)
        
    def anuluj(self):
        self.done(0)