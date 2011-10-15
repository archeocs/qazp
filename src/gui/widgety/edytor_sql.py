'''
Created on Jul 28, 2011

@author: milosz
'''

from PyQt4.QtGui import QDialog, QDialogButtonBox,QVBoxLayout,QPlainTextEdit
from PyQt4.QtCore import SIGNAL


class EdytorSql(QDialog):

    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.anulowany = True
        vbox = QVBoxLayout(self)
        self.txt_edytor = QPlainTextEdit(self)
        vbox.addWidget(self.txt_edytor)
        self.btnbox = QDialogButtonBox(self)
        self.btnbox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        vbox.addWidget(self.btnbox)
        self.connect(self.btnbox, SIGNAL("accepted()"),self.zatwierdz)
        self.connect(self.btnbox, SIGNAL("rejected()"),self.anuluj)
        
    def anuluj(self):
        self.anulowany = True
        self.done(0)
        
    def zatwierdz(self):
        self.anulowany = False
        self.done(1)
        
    def get_tekst(self):
        if not self.anulowany:
            return unicode(self.txt_edytor.toPlainText())
        return None    
        
class BladSql(EdytorSql):
    
    def __init__(self,blad,parent=None):
        EdytorSql.__init__(self,parent)
        self.btnbox.setStandardButtons(QDialogButtonBox.Close)
        self.txt_edytor.setPlainText(blad)
        self.txt_edytor.setReadOnly(True)
                