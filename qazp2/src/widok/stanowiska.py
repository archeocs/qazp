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
    rejestr_map, stLista, sqlListaId
from widok.sted import Edytor
from lib.keza import  KezaDruk
from widok.dialog import NrAzpDialog
from lib.qgsop import usun, tempWarstwa
from widok.filtred import FiltrWidget

def tab_model(obiekty,parent=None):
    return GTabModel2([('Ident','id'),('Obszar','obszar'),('Nr na obszarze','nr_obszar'),('Rodzaj','rodzaj_badan')
                      ,('Data','data'),('Autor','autor'),('Uwagi','uwagi')],obiekty,parent)
    
    
class StanowiskaFrame(GFrame):
    
    warstwa = None
    def __init__(self, warstwa, listaSt, iface, win, parent=None):
        GFrame.__init__(self,win,listaSt)
        self.setObjectName('stanowiska')
        self.warstwa = warstwa
        self._if = iface
        self._win = win
        self._win.statusBar().showMessage("Wyszukano %s obiektow %s"%(str(self.warstwa.featureCount()),
               self.warstwa.dataProvider().dataSourceUri()))
        self._con = getPolaczenie2(self.warstwa)
        
    def akcja_wyswietl(self):
        atrs = self.warstwa.dataProvider().fields()
        nv = tempWarstwa(self.wszystkie(), "filtr_"+self.warstwa.name(), "Polygon", atrs)
        nv.setCrs(self.warstwa.crs())
        if rejestr_map().addMapLayer(nv):
            QMessageBox.information(self,'info','Do projektu zostala dodana warstwa '+nv.name())
    
    def utworz_model(self, gobs):
        return tab_model(gobs, self)
    
    def akcja_zmien(self):
        ww = self.wybrany_wiersz()[1]
        ed = Edytor(self.warstwa, ww, self._win, funModel=self.zmienWiersz)
        self._win.setWindowTitle('Stanowisko: '+str(ww['obszar'].toString())+'/'+str(ww['nr_obszar'].toString()))
        self._win.dodaj(ed)
        
    def _akcjaDrukuj(self):
        #kd = KezaDruk(getPolaczenie2(self.warstwa))
        kd = KezaDruk(self._con)
        plik = QFileDialog.getSaveFileName(parent=self, filter='PDF (*.pdf)')
        pd = QProgressDialog("Przygotowuje wydruk", "Cancel", 0, len(self._gobs)+1);
        pd.setWindowModality(Qt.WindowModal);
        sts = []
        for st in self.wszystkie():
            cent = st.wspolrzedne().centroid()#.asPoint()
            if cent is None:
                raise Exception("Centroid jest NONE "+str(st['id'].toInt()[0]))
            else:
                ptc = cent.asPoint()
                sts.append((st['id'].toInt()[0], unicode(st['obszar'].toString()), unicode(st['nr_obszar'].toString()),
                            round(ptc.x(),2), round(ptc.y(),2)))
        kd.drukuj(plik, sts, pd)
        QMessageBox.information(self,'Drukowanie','Karty wygenerowane')
    
    def _anulujFiltr(self):
        #self._con.zakoncz()
        self._win.usun()
    
    def _zastosujFiltr(self, mapa):
        self._win.usun()
        fzbior = None
        for (k, m) in mapa.iteritems():
            rf = k.filtr(m)
            s = sqlListaId(self._con, rf[0], rf[1])
            if fzbior is None:
                fzbior = s
            else:
                fzbior &= s # przekroj zbiorow - interesujace sa tylko powtarzajace sie identyfikatory
        f = self.setFiltr(fzbior)
        QMessageBox.information(self,'Filtrowanie','Filtr zastosowany. Wybrano '+str(f))
    
    def _akcjaFiltruj(self):
        fw = FiltrWidget(self._con)
        fw.filtruj.connect(self._zastosujFiltr)
        fw.anuluj.connect(self._anulujFiltr)
        self._win.dodaj(fw)
        
    def akcja_usun(self):
        ww = self.wybrany_wiersz()
        odp = QMessageBox.question(self, u'Usuwanie stanowiska', u'Czy na pewno chcesz usunąć stanowisko %d'%ww[1]['id'].toInt()[0],
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if odp != QMessageBox.Yes:
            return
        if usun(self.warstwa, ww[1].feature()):
            self.getModel().removeRow(ww[0].row())
            self._win.statusBar().showMessage(u'Stanowisko usunięte')

    def _akcjaOk(self):
        self._con.zakoncz()
        self._win.usun()

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
        #db = getPolaczenie2(get_warstwa('stanowiska'))
        if self._con._con.isOpen():
            QMessageBox.information(self, u'Połączenie', 'Połączenie nawiązane')
        