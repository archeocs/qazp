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

from PyQt4.QtGui import QAction, QApplication,QMainWindow,QStackedWidget
from PyQt4.QtCore import QObject, SIGNAL
from widok import trasy,miejsca,stanowiska, wykazy

class Okno(QMainWindow):
    
    def __init__(self,parent=None,iface=None):
        QMainWindow.__init__(self,parent)
        self._iface = iface
        self.menu()
        self.statusBar().showMessage("ok")
        self.zapamietane = []
        self.setWindowTitle('qazp2')
        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)
        
    def menu(self):
        miej_menu = self.menuBar().addMenu('Miejsca')
        miej_menu.addAction(miejsca.WyszukajAkcja(self._iface,self))
        miej_menu.addAction(miejsca.ImportGpsAkcja(self._iface,self))
        miej_menu.addAction(miejsca.TestUri(self._iface,self))
        trasy_menu = self.menuBar().addMenu('Trasy')
        trasy_menu.addAction(trasy.WyszukajAkcja(self._iface,self))
        trasy_menu.addAction(trasy.ImportGpsAkcja(self._iface,self))
        stan_menu = self.menuBar().addMenu('Stanowiska')
        stan_menu.addAction(stanowiska.WyszukajAkcja(self._iface,self))
        stan_menu.addAction(stanowiska.PolaczSql(self._iface,self))
        wykaz_menu = self.menuBar().addMenu('Wykazy')
        wykaz_menu.addAction(wykazy.WykazAkcja(u'Miejscowości','miejscowosci',self._iface,self))
        wykaz_menu.addAction(wykazy.WykazAkcja(u'Gminy','gminy',self._iface,self))
        wykaz_menu.addAction(wykazy.WykazAkcja(u'Powiaty','powiaty',self._iface,self))
        wykaz_menu.addAction(wykazy.WykazAkcja(u'Województwa','wojewodztwa',self._iface,self))
        
    
    def dodaj(self,wgt):
        self._stack.addWidget(wgt)
        self._stack.setCurrentWidget(wgt)
        
    def usun(self,wgt=None):
        if wgt is None:
            self._stack.removeWidget(self._stack.count()-1)
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
    
if __name__ == '__main__':
    from sys import argv
    app = QApplication(argv)
    start(app=app)
    
