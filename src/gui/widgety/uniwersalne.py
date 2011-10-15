from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Siatka(QGridLayout):
    
    ik = 2
    ostatni = None
    def __init__(self,ile_kolumn=2): # ile_kolumn - ile kolumn w siatce
        QGridLayout.__init__(self)
        self.ik = ile_kolumn
        self.setAlignment(Qt.AlignTop)
        #self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding,QSizePolicy.Minimum)

    def nowy_spacer(self):
        return QSpacerItem(40, 20, QSizePolicy.Expanding,QSizePolicy.Minimum) 
        
    def dodaj_widget(self,widget,etykieta): #addWidget(w,row,col)
        if self.ostatni is None:
            self.ostatni = (0,1)
        elif self.ostatni[1] == self.ik:
            self.ostatni = (self.ostatni[0]+1,1)
        else:
            self.ostatni = (self.ostatni[0],self.ostatni[1]+1)
        sp = self.ostatni[1] * 3 - 1 # pozycja spacera
        wp = sp - 1 # pozycja widgetu
        ep = wp - 1 # pozycja etykiety
        self.addWidget(QLabel(QApplication.translate("MainWindow", etykieta, None,QApplication.UnicodeUTF8)),self.ostatni[0],ep)
        self.addWidget(widget,self.ostatni[0],wp)
        self.addItem(self.nowy_spacer(),self.ostatni[0],sp,1,1)
        return widget
        
class Grupa(QGroupBox):

    def __init__(self,ile_kolumn=2,tytul=None):
        QGroupBox.__init__(self)
        self.grid = Siatka(ile_kolumn)
        self.setLayout(self.grid)
        if tytul is not None:
            self.setTitle(tytul)
        
    def dodaj_widget(self,widget,etykieta):
        return self.grid.dodaj_widget(widget,etykieta)
        
class StronaSiatka(QWidget):
    def __init__(self,ile_kolumn=2):
        QWidget.__init__(self)
        self.grid = Siatka(ile_kolumn)
        self.setLayout(self.grid)
        
    def dodaj_widget(self,widget,etykieta):
        return self.grid.dodaj_widget(widget,etykieta)
        
class StronaGrupy(QWidget):
    
    def __init__(self):
        QWidget.__init__(self)
        self.vb = QVBoxLayout()
        self.setLayout(self.vb)
        
    def dodaj_grupe(self,ile_kolumn=2,tytul=None):
        g = Grupa(ile_kolumn,tytul)
        self.vb.addWidget(g)
        return g
            