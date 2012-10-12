'''
Created on Sep 9, 2012

@author: milosz
'''

from PyQt4.QtGui import QAction, QApplication,QMainWindow,QStackedWidget
from PyQt4.QtCore import QObject, SIGNAL
from widok import trasy,miejsca,stanowiska

class Okno(QMainWindow):
    
    def __init__(self,parent=None,iface=None):
        QMainWindow.__init__(self,parent)
        self._iface = iface
        self.menu()
        self.statusBar().showMessage("ok")
        self.zapamietane = []
        self.setWindowTitle('qazp 8')
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
        
    #===========================================================================
    # def zapamietaj(self,wgt):
    #    self.zapamietane.append(wgt)
    #    
    # def przywroc(self):
    #    #raise Exception('brak impl')
    #    if self.zapamietane:
    #        z = self.zapamietane.pop()
    #        if z is None:
    #            raise Exception('pusty zapamietany')
    #        z.setVisible(True)
    #        self.setCentralWidget(z)
    #        self.statusBar().showMessage(z.objectName())
    #    else:
    #        raise Exception('brak zapamietanych')
    #===========================================================================
    
    def dodaj(self,wgt):
        self._stack.addWidget(wgt)
        self._stack.setCurrentWidget(wgt)
        
    def usun(self,wgt=None):
        if wgt is None:
            self._stack.removeWidget(self._stack.count()-1)
        else:
            self._stack.removeWidget(wgt)
    
    #===========================================================================
    # def setCentralWidget(self, wgt):
    #    biez = self.centralWidget()
    #    if biez is not None:
    #        self.zapamietaj(biez)
    #    QMainWindow.setCentralWidget(self,wgt)
    #    if self.zapamietane:
    #        self.statusBar().showMessage('zapamietany '+str(self.zapamietane[0].objectName())+" "+str(len(self.zapamietane)))
    #===========================================================================

class QazpPlugin(object):
    
    def __init__(self,iface):
        self.iface = iface
    
    def initGui(self):
        self.akcja = QAction("Test QAZP2", self.iface.mainWindow())
        self.akcja.setWhatsThis("Test QAZP2")
        self.akcja.setStatusTip("qazp2")
        QObject.connect(self.akcja, SIGNAL("triggered()"), self.run)

        self.iface.addToolBarIcon(self.akcja)
        self.iface.addPluginToMenu("TQ",self.akcja)
    
    def unload(self):
        self.iface.removePluginMenu("TQ",self.akcja)
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
    
