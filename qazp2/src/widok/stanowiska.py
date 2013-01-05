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

from PyQt4.QtCore import SIGNAL,QObject,Qt
from PyQt4.QtGui import QAction,QMessageBox,QInputDialog, QProgressDialog, QFileDialog, QDialog
from widok.lista import GTabModel2, GFrame
from dane.zrodla import gstanowiska, get_warstwa, szukaj_stanowiska,getPolaczenie2,\
    rejestr_map, stLista
from widok.sted import Edytor
from lib.keza import GeneratorKeza
from widok.dialog import NrAzpDialog

def tab_model(obiekty,parent=None):
    return GTabModel2([('Ident','id'),('Obszar','obszar'),('Nr na obszarze','nr_obszar'),('Rodzaj','rodzaj_badan')
                      ,('Data','data'),('Autor','autor'),('Uwagi','uwagi')],obiekty,parent)
    
    
class StanowiskaFrame(GFrame):
    
    warstwa = None
    def __init__(self,warstwa,listaSt,iface,win,parent=None):
        GFrame.__init__(self,win,listaSt)
        self.setObjectName('stanowiska')
        self.warstwa = warstwa
        self._if = iface
        self._win = win
        self._win.statusBar().showMessage("Wyszukano %s obiektow %s"%(str(self.warstwa.featureCount()),
                                                                      self.warstwa.dataProvider().dataSourceUri()))
    
    def akcja_wyswietl(self):
        if self.warstwa is not None:
            rejestr_map().addMapLayer(self.warstwa)
            QMessageBox.information(self,'info','Do projektu zostala dodana warstwa '+self.warstwa.name())    
    
    def utworz_model(self, gobs):
        return tab_model(gobs, self)
    
    def akcja_zmien(self):
        ww = self.wybrany_wiersz()[1]
        ed = Edytor(self.warstwa,ww,self._win,funModel=self.zmienWiersz)
        self._win.setWindowTitle('Stanowisko: '+str(ww['obszar'].toString())+'/'+str(ww['nr_obszar'].toString()))
        self._win.dodaj(ed)
        
    def _akcjaDrukuj(self):
        gen = GeneratorKeza(getPolaczenie2(self.warstwa))
        plik = QFileDialog.getSaveFileName(parent=self, filter='PNG (*.pdf)')
        pd = QProgressDialog("Przygotowuje wydruk", "Cancel", 0, len(self._gobs)+1);
        pd.setWindowModality(Qt.WindowModal);
        c = 0
        for st in self.wszystkie():
            c+=1
            pd.setValue(c)
            pd.setLabelText(u'Stanowisko %s/%s'%(unicode(st['obszar'].toString()),unicode(st['nr_obszar'].toString())))
            sid = st['id'].toInt()[0]
            cent = st.wspolrzedne().centroid().asPoint()
            wsp = {'x':round(cent.x(),2), 'y':round(cent.y(),2)}
            gen.dodajKarte(sid,wsp)
        gen.zapisz(str(plik))
        pd.setValue(len(self._gobs)+1)
        QMessageBox.information(self,'Drukowanie','Karty wygenerowane')

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
        warunek = QInputDialog.getText(self._win, 'Stanowiska', 'Wprowadz warunek', text="obszar='56-27' and nr_obszar='1'")
        if warunek[1]:
            warstwa = szukaj_stanowiska(unicode(warunek[0]))
            mf = StanowiskaFrame(warstwa,gstanowiska(warstwa),self._iface,self._win)
            self._win.dodaj(mf)

class WyszukajNrAzpAkcja(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,u'Wyszukaj wg numeru AZP',window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        trasy = get_warstwa('stanowiska')
        if trasy is None:
            QMessageBox.warning(self._win,u'Wyszukaj',u'Przed wyszukiwaniem należy otworzyć warstwę "stanowiska"')
            return 
        #warunek = QInputDialog.getText(self._win, 'Stanowiska', 'Wprowadz warunek', text="obszar='56-27' and nr_obszar='1'")
        dialog = NrAzpDialog(self._win)
        if dialog.exec_() != QDialog.Accepted:
            return
        dane = dialog.getDane()
        warunek = "obszar='%(obszar)s' and nr_obszar='%(nr_obszar)s'" % dane
        if dane['data_od'] != '':
            szukDt = '1900-01-01'
            if len(dane['data_od']) == 4:
                szukDt = '%s-01-01'%dane['data_od']
            elif len(dane['data_od']) == 7:
                szukDt = '%s-01'%dane['data_od']
            elif len(dane['data_od']) == 10:
                szukDt = dane['data_od']
            warunek += " and data >= '%s'"%szukDt
        warstwa = szukaj_stanowiska(unicode(warunek))
        mf = StanowiskaFrame(warstwa,gstanowiska(warstwa),self._iface,self._win)
        self._win.dodaj(mf)


class PokazujZaznAkcja(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,'Pokazuj zaznaczone',window)
        self.triggered.connect(self.wykonaj)
        #QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        self.setCheckable(True)
    
    def wykonaj(self):
        sts = get_warstwa('stanowiska')
        sts.selectionChanged.connect(self._pokWybrane)
    
    def _pokWybrane(self):
        sts = get_warstwa('stanowiska')
        lista = sts.selectedFeatures()
        if len(lista) > 0:
            mf = StanowiskaFrame(sts,stLista(lista),self._iface,self._win)
            self._win.pokazZaznaczone(mf)
        
class PolaczSql(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,u'Połączenie',window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        db = getPolaczenie2(get_warstwa('stanowiska'))
        if db._con.isOpen():
            QMessageBox.information(self, u'Połączenie', 'Połączenie nawiązane')
        