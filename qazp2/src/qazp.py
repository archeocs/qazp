# -*- coding: utf-8 -*-

# QAZP2 
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

from PyQt4.QtGui import QAction, QApplication,QMainWindow,QStackedWidget, QMessageBox,\
                        QFileDialog
from PyQt4.QtCore import QObject, SIGNAL
from widok import trasy,miejsca,stanowiska, wykazy, admin, zestawienia
from qgis.core import QgsMapLayerRegistry
from os.path import abspath
from dane.zrodla import get_warstwa, getPolaczenie2
from lib.uzytki import dostosujSchemat, wykonajPolecenie


class SchematAkcja(QAction):
    def __init__(self,iface,window):
        QAction.__init__(self,'Dostosuj schemat',window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        warstwa = get_warstwa('stanowiska')
        if warstwa is None:
            QMessageBox.warning(self._win,u'Dostosuj schemat',u'Przed wyszukiwaniem należy otworzyć warstwę "stanowiska"')
            return 
        pytanie = QMessageBox.question(self._win, u'Dostosuj schemat', u'Czy została wykonana kopia zapasowa bazy?\n'\
                                       u'Czy na pewno chcesz zmodyfikować schemat bazy danych?', QMessageBox.Yes | QMessageBox.No, 
                                       QMessageBox.No)
        if pytanie == QMessageBox.Yes:
            con = getPolaczenie2(warstwa)
            if dostosujSchemat(con):
                self._win.statusBar().showMessage("Schemat zmieniony")
            else:
                self._win.statusBar().showMessage("Niepowodzenie")
            con.zakoncz()

class SkryptAkcja(QAction):
    def __init__(self,iface,window):
        QAction.__init__(self,'Wykonaj skrypt',window)
        #QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self.triggered.connect(self.wykonaj)
        self._win = window
        self._iface = iface
    
    def uruchomSkrypt(self, con, plik):
        import json
        f = open(plik)
        skrypt = json.load(f)
        for s in skrypt:
            if wykonajPolecenie(con, s['stmt']) != s['wynik']:
                con.wycofaj()
                f.close()
                return False
        con.zatwierdz()
        f.close()
        return True
        
    def wykonaj(self):
        warstwa = get_warstwa('stanowiska')
        if warstwa is None:
            QMessageBox.warning(self._win,u'Wykonaj skrypt',u'Przed wyszukiwaniem należy otworzyć warstwę "stanowiska"')
            return 
        fn = QFileDialog.getOpenFileName(self._win, filter='JSQL (*.jsql)')
        if fn is None or str(fn) == "":
            return
        pytanie = QMessageBox.question(self._win, u'Wykonaj skrypt', u'Czy została wykonana kopia zapasowa bazy?\n'\
                                       u'Czy na pewno chcesz wykonać skrypt?', QMessageBox.Yes | QMessageBox.No, 
                                       QMessageBox.No)
        if pytanie == QMessageBox.Yes:
            con = getPolaczenie2(warstwa)
            if self.uruchomSkrypt(con, str(fn)):
                self._win.statusBar().showMessage("Zmiany wprowadzone")
            else:
                self._win.statusBar().showMessage("Niepowodzenie")
            con.zakoncz()

class Okno(QMainWindow):
    
    def __init__(self,parent=None,iface=None):
        QMainWindow.__init__(self,parent)
        self._iface = iface
        self.menu()
        self.statusBar().showMessage("ok")
        self.zapamietane = []
        self.setWindowTitle('qazp 0.14.3')
        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)
        
    def menu(self):
        miej_menu = self.menuBar().addMenu('Miejsca')
        miej_menu.addAction(miejsca.WyszukajAkcja(self._iface, self))
        miej_menu.addAction(miejsca.ImportGpsAkcja(self._iface, self))
        miej_menu.addAction(miejsca.TestUri(self._iface, self))
        trasy_menu = self.menuBar().addMenu('Trasy')
        trasy_menu.addAction(trasy.WyszukajAkcja(self._iface, self))
        trasy_menu.addAction(trasy.ImportGpsAkcja(self._iface, self))
        stan_menu = self.menuBar().addMenu('Stanowiska')
        stan_menu.addAction(stanowiska.WyszukajAkcja(self._iface, self))
        stan_menu.addAction(stanowiska.WyszukajNrAzpAkcja(self._iface, self))
        #stan_menu.addAction(stanowiska.PolaczSql(self._iface,self))
        stan_menu.addAction(stanowiska.PokazujZaznAkcja(self._iface, self))
        wykaz_menu = self.menuBar().addMenu('Wykazy')
        wykaz_menu.addAction(wykazy.WykazAkcja(u'Miejscowości','miejscowosci', self._iface, self))
        wykaz_menu.addAction(wykazy.WykazAkcja(u'Gminy','gminy', self._iface, self))
        wykaz_menu.addAction(wykazy.WykazAkcja(u'Powiaty','powiaty', self._iface, self))
        wykaz_menu.addAction(wykazy.WykazAkcja(u'Województwa','wojewodztwa', self._iface, self))
        admin_menu = self.menuBar().addMenu('Administracja')
        admin_menu.addAction(admin.SchematAkcja(self._iface, self))
        admin_menu.addAction(admin.SkryptAkcja(self._iface, self))
        admin_menu.addAction(admin.LogowanieAkcja(self._iface, self))
        zest_menu = self.menuBar().addMenu('Zestawienia')
        zest_menu.addAction(zestawienia.NoweZestawienieAkcja(self._iface, self))
        fakty_sub = zest_menu.addMenu('Fakty osadnicze')
        fakty_sub.addAction(zestawienia.jednostkiObszar(self._iface, self))
        fakty_sub.addAction(zestawienia.jedOkrObszar(self._iface, self))
        fakty_sub.addAction(zestawienia.jedOkrFunObszar(self._iface, self))
        fakty_sub.addAction(zestawienia.jednostkiMiej(self._iface, self))
        fakty_sub.addAction(zestawienia.jedOkrMiej(self._iface, self))
        fakty_sub.addAction(zestawienia.jedOkrFunMiej(self._iface, self))
    
    zaznWgt = None
    def pokazZaznaczone(self,wgt):
        if self.zaznWgt:
            self._stack.removeWidget(self.zaznWgt)
        self.zaznWgt = wgt
        self.dodaj(wgt)
    
    def dodaj(self,wgt):
        self._stack.addWidget(wgt)
        self._stack.setCurrentWidget(wgt)
        
    def usun(self,wgt=None):
        if wgt is None:
            self._stack.removeWidget(self._stack.currentWidget())
        else:
            self._stack.removeWidget(wgt)
            
class QazpPlugin(object):
    
    def __init__(self,iface):
        self.iface = iface
    
    def initGui(self):
        self.akcja = QAction("QAZP2", self.iface.mainWindow())
        self.akcja.setWhatsThis("QAZP2")
        self.akcja.setStatusTip("qazp2")
        QObject.connect(self.akcja, SIGNAL("triggered()"), self.run)

        self.iface.addToolBarIcon(self.akcja)
        self.iface.addPluginToMenu("QAZP2",self.akcja)
        QgsMapLayerRegistry.instance().layerWasAdded.connect(self._dodajUi)
    
    def _dodajUi(self,mapa):
        if str(mapa.name()).startswith('miejsca'):
            mapa.setEditForm(abspath(__file__+'/../forms/miejsca.ui'))
        elif str(mapa.name()).startswith('stanowiska'):
            mapa.setEditForm(abspath(__file__+'/../forms/stanowiska.ui'))
        elif str(mapa.name()).startswith('trasy'):
            mapa.setEditForm(abspath(__file__+'/../forms/trasy.ui'))
    
    def unload(self):
        self.iface.removePluginMenu("QAZP2",self.akcja)
        self.iface.removeToolBarIcon(self.akcja)
        
    def run(self):
        start(self.iface.mainWindow(),self.iface)
        
def start(mw=None,iface=None,app=None):
    td = Okno(mw,iface)
    td.show()
    if app:
        app.exec_()