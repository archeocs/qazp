'''
Created on Sep 9, 2012

@author: milosz
'''

from PyQt4.QtGui import QMainWindow, QFrame, QVBoxLayout, QPushButton,QMessageBox,QLineEdit
from PyQt4.QtCore import SIGNAL
from dane.zrodla import Warstwa

class TestDial(QMainWindow):
    
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent=parent)
        self.frame = QFrame(self)
        self.setCentralWidget(self.frame)
        vbox = QVBoxLayout(self.frame)
        self.txt = QLineEdit()
        btn_sel = QPushButton(u'Szukaj',self.frame)
        vbox.addWidget(self.txt)
        vbox.addWidget(btn_sel)
        self.frame.connect(btn_sel, SIGNAL('clicked(bool)'),self.sel_action)
        
    def sel_action(self):
        w = Warstwa("miejsca")
        nw = w.szukaj(self.txt)
        QMessageBox.information(self.frame, 'abc', str(nw.featureCount()))