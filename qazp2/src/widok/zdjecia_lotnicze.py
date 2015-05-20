# -*- coding: utf-8 -*-

# 20qazp
# (c) Milosz Piglas 2014 Wszystkie prawa zastrzezone

# Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
# 
#      * Redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above
#  copyright notice, this list of conditions and the following disclaimer
#  in the documentation and/or other materials provided with the
#  distribution.
#      * Neither the name of 20qazp nor the names of its
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
from dane.zrodla import gzdjecia, get_warstwa, szukaj_zdjecia,getPolaczenie2,\
    rejestr_map, stLista, sqlListaId
from lib.qgsop import usun, tempWarstwa

def tab_model(obiekty,parent=None):
    return GTabModel2([('Ident','id'),('Folder','folder'),('Klatka','klatka') ,('Data','data'),
                       ('Autor','autor')],obiekty,parent)

class ListaZdjec(GFrame):

    def __init__(self, warstwa, lista, iface, win, parent=None):
        GFrame.__init__(self, win, lista, parent)
        self.setObjectName(u'Zdjęcia lotnicze')
        self.warstwa = warstwa
        self._if = iface
        self._win = win
        self._win.statusBar().showMessage("Wyszukano %s obiektow %s"%(str(self.warstwa.featureCount()),
               self.warstwa.dataProvider().dataSourceUri()))
        self._con = getPolaczenie2(self.warstwa)

    def akcja_wyswietl(self):
        atrs = self.warstwa.dataProvider().fields()
        nv = tempWarstwa(self.wszystkie(), "filtr_"+self.warstwa.name(), "Point", atrs)
        nv.setCrs(self.warstwa.crs())
        if rejestr_map().addMapLayer(nv):
            QMessageBox.information(self,'info','Do projektu zostala dodana warstwa '+nv.name())

    def utworz_model(self, gobs):
        return tab_model(gobs, self)

    def akcja_zmien(self):
        pass
        #ww = self.wybrany_wiersz()[1]
        #ed = Edytor(self.warstwa, ww, self._win, funModel=self.zmienWiersz)
        #self._win.setWindowTitle('Stanowisko: '+str(ww['obszar'])+'/'+str(ww['nr_obszar']))
        #self._win.dodaj(ed)

    def _akcjaDrukuj(self):
        pass

    def _akcjaFiltruj(self):
        pass

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
        trasy = get_warstwa('zdjecia_lotnicze')
        if trasy is None:
            QMessageBox.warning(self._win,u'Wyszukaj',u'Przed wyszukiwaniem należy otworzyć warstwę "zdjecia_lotnicze"')
            return
        warunek = QInputDialog.getText(self._win, u'Zdjęcie', u'Wprowadź warunek', text="folder='2014_07_23' and klatka='DSC_0119'")
        if warunek[1]:
            warstwa = szukaj_zdjecia(unicode(warunek[0]))
            mf = ListaZdjec(warstwa,gzdjecia(warstwa),self._iface,self._win)
            self._win.dodaj(mf)