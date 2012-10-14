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

'''
Created on Sep 9, 2012

@author: milosz
'''

from lista import GTabModel, GFrame
from PyQt4.QtGui import QMessageBox, QAction, QVBoxLayout QDialogButtonBox, QLineEdit
from PyQt4.QtGui import QInputDialog, QFileDialog ,QFrame
from PyQt4.QtCore import QObject,SIGNAL,
from lib.qgsop import zmien, usun, dodaj, setMapa
from lib.gps import WayPoints
from dane.zrodla import rejestr_map, get_warstwa, gmiejsca, szukaj_miejsca
from qgis.core import QgsDataSourceURI
from functools import partial
from os.path import abspath
from widok.proped import PropWidok, conw
from dane.model import MIEJSCA_ATR


def tab_model(obiekty,parent=None):
    return GTabModel(['Ident','Nazwa','Rodzaj','Data','Autor','Uwagi'],obiekty,parent)
    
class MiejscaWidokEd(PropWidok):
    
    vrd = [('P',u'Powierzchniowe'),('W',u'Weryfikacja'),('L',u'Lotnicze')]
    wrd = partial(conw,slow=dict(vrd))
    def __init__(self,dane,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Nazwa','nazwa',self.nic),(u'Rodzaj','rodzaj_badan',self.wrd),('Data','data',self.nic),
             (u'Autor','autor',self.nic),(u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        self.dodajOpt(1, self.vrd)

class MiejscaEdytor(QFrame):
    
    def __init__(self, warstwa, dane, win, parent=None):
        QFrame.__init__(self,parent)
        self._dane = dane
        self._win = win
        self._war = warstwa
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self._widok = MiejscaWidokEd(self._dane,self)
        vbox.addWidget(self._widok)
        bb = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close)
        bb.accepted.connect(self._zapisz)
        bb.rejected.connect(self._zamknij)
        vbox.addWidget(bb)
        
    def _zapisz(self):
        obj = self._dane.feature()
        setMapa(obj, self._widok.wartosci(), MIEJSCA_ATR)
        if zmien(self._war,obj):
            self._win.statusBar().showMessage('Zapisano zmiany')
        else:
            self._win.statusBar().showMessage('Blad zapisu')
    
    def _zamknij(self):
        self._win.usun(self)

class MiejscaFrame(GFrame):
    
    warstwa = None
    def __init__(self, warstwa, iface, win, parent=None):
        GFrame.__init__(self,win,gmiejsca(warstwa))
        self.setObjectName('miejsca')
        self.warstwa = warstwa
        self._if = iface
        self._win = win
        self._win.statusBar().showMessage("Wyszukano %s obiektow %s"%(str(self.warstwa.featureCount()),
                                                                      self.warstwa.dataProvider().dataSourceUri()))
        
    def utworz_model(self, gobs):
        return tab_model(gobs, self)
        
    def akcja_wyswietl(self):
        if self.warstwa is not None:
            rejestr_map().addMapLayer(self.warstwa)
            QMessageBox.information(self,'info','Do projektu zostala dodana warstwa '+self.warstwa.name())
        
    def akcja_zmien(self):
        ww = self.wybrany_wiersz()[1]
        self._win.dodaj(MiejscaEdytor(self.warstwa,ww,self._win))
                
    def akcja_usun(self):
        ww = self.wybrany_wiersz()[1]
        u = usun(self.warstwa,ww.feature())
        if u:
            QMessageBox.information(self, 'info', u'Usuniete miejsce %s'%unicode(ww['nazwa'].toString()))
            
def formularz(dialog,fid,feature):
    txtNaz = dialog.findChild(QLineEdit,"nazwa")
    txtNaz.setText(u'Nowa')

class WyszukajAkcja(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,'Wyszukaj',window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        trasy = get_warstwa('miejsca')
        if trasy is None:
            QMessageBox.warning(self._win,u'Wyszukaj',u'Przed wyszukiwaniem należy otworzyć warstwę "miejsca"')
            return 
        warunek = QInputDialog.getText(self._win, 'Miejsca', 'Wprowadz warunek', text='id > 0')
        if warunek[1]:
            mf = MiejscaFrame(szukaj_miejsca(unicode(warunek[0])),self._iface,self._win)
            self._win.dodaj(mf)

class ImportGpsAkcja(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,'Importuj z GPS',window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        trasy = get_warstwa('miejsca')
        if trasy is None:
            QMessageBox.warning(self._win,u'Import z GPS',u'Przed importem należy otworzyć warstwę "miejsca"')
            return 
        if self._iface:
            fn = QFileDialog.getOpenFileName(self._win, filter='Pliki GPX (*.gpx)')
        else:
            fn = '/home/milosz/archeocs/gpx/miejsca_test.gpx'
        wp = WayPoints()
        wp.create(fn)
        if self._iface is None:
            QMessageBox.information(self._win, 'Import GPS', 'Odczytano %d punktow'%len(wp.pts_list))
            return
        miejsca = get_warstwa("miejsca")
        miejsca.startEditing()
        for (pi,p) in enumerate(wp.pts_list):
            m = p.mapa()
            m[1] = 'punkt %d'%pi
            dodaj(miejsca, m, p.geom())
        if miejsca.commitChanges():
            QMessageBox.information(self._win, 'Import GPS', 'Zapisano %d punktow'%len(wp.pts_list))

class TestUri(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,'Test uri',window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface  
        
    def wykonaj(self):
        mw = get_warstwa("miejsca")
        QMessageBox.information(self._win, 'test', QgsDataSourceURI(mw.dataProvider().dataSourceUri()).sql())
        
    
        
    