'''
Created on Sep 9, 2012

@author: milosz
'''

from PyQt4.QtGui import QAction, QApplication,QMainWindow
from PyQt4.QtCore import QObject, SIGNAL
from widok import trasy,miejsca

class Okno(QMainWindow):
    
    def __init__(self,parent=None,iface=None):
        QMainWindow.__init__(self,parent)
        self._iface = iface
        self.menu()
        self.statusBar().showMessage("ok")
        self.setFixedSize(700,500)
        
    def menu(self):
        miej_menu = self.menuBar().addMenu('Miejsca')
        miej_menu.addAction(miejsca.WyszukajAkcja(self._iface,self))
        miej_menu.addAction(miejsca.ImportGpsAkcja(self._iface,self))
        miej_menu.addAction(miejsca.TestUri(self._iface,self))
        trasy_menu = self.menuBar().addMenu('Trasy')
        trasy_menu.addAction(trasy.WyszukajAkcja(self._iface,self))
        trasy_menu.addAction(trasy.ImportGpsAkcja(self._iface,self))

class QazpPlugin(object):
    
    def __init__(self,iface):
        self.iface = iface
    
    def initGui(self):
        self.akcja = QAction("QAZP2", self.iface.mainWindow())
        self.akcja.setWhatsThis("QAZP2")
        self.akcja.setStatusTip("qazp2")
        QObject.connect(self.akcja, SIGNAL("triggered()"), self.run)

        self.iface.addToolBarIcon(self.akcja)
        self.iface.addPluginToMenu("QZP2",self.akcja)
    
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
    
