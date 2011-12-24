from PyQt4.QtGui import QPlainTextEdit,QStyledItemDelegate,QComboBox,QSpinBox,QTableWidget
from PyQt4.QtGui import QWidget, QVBoxLayout, QAbstractItemView, QTableWidgetItem,QApplication,QHeaderView
from PyQt4.QtCore import Qt,SIGNAL

class FaktyEdytor(QStyledItemDelegate):
    
    def __init__(self,stan,dane,parent=None):
        QStyledItemDelegate.__init__(self,parent)
        self.stan = stan
        self.dane = dane
        self.fakty = []
        
    def _createCombo(self,parent,lista,wybrany=0):
        combo_ed = QComboBox(parent)
        combo_ed.clear()
        combo_ed.addItem(u'Nieokreslona')
        combo_ed.addItems(lista)
        combo_ed.setCurrentIndex(wybrany)
        return combo_ed
        
    def _createPte(self,parent):
        pte_ed = QPlainTextEdit(parent)
        pte_ed.setFixedSize(200,100)
        return pte_ed
    
    def _createSpin(self,parent):
        spin_ed = QSpinBox(parent)
        spin_ed.setFixedWidth(40)
        return spin_ed
    
    def createEditor(self,parent,opcje,indeks):
        #return QPlainTextEdit(parent)
        k = indeks.column()
        w = indeks.row()
        fep,fku,ffu = 0,0,0
        wyb = 0
        if w < len(self.fakty):
            f = self.fakty[w]
            fep,fku,ffu = f.epoka,f.kultura,f.funkcja
            nep,nku,nfu = f.epoka_nazwa, f.kultura_nazwa, f.funkcja_nazwa
            #print unicode(f)
        if k == 0:
            if fep > 0:
                #wyb = self.epoki.indeks_sid(fep-1)
                wyb = self.epoki.nazwa_ind(nep)+1
            return self._createCombo(parent, self.epoki.lista(),wyb)
        elif k == 1:
            if fku > 0:
                #wyb = self.kultury.indeks_sid(fku-1)
                wyb = self.kultury.nazwa_ind(nku)+1
            return self._createCombo(parent, self.kultury.lista(),wyb)
        elif k == 2:
            if ffu > 0:
                #wyb = self.funkcje.indeks_sid(ffu-1)
                wyb = self.funkcje.nazwa_ind(nfu)+1
            return self._createCombo(parent, self.funkcje.lista(),wyb)
        elif k == 3 or k == 4 :
            return self._createPte(parent)
        else:
            return self._createSpin(parent)    
    
    def dodajFakt(self,fakt):
        self.fakty.append(fakt)
        
    def nieokresl(self,cb,slo):
        i = cb.currentIndex()
        if i < 1:
            return (0,u'Nieokreslona')
        else:
            nazwa = unicode(cb.currentText())
            slow_id = slo.nazwa_sid(nazwa)
            return (slow_id,nazwa)    
        
    def setModelData(self, editor, model, index):
        k = index.column()
        w = index.row()
        if w >= len(self.fakty):
            self.fakty.append(self.dane.nowy_fakt(self.stan))
        if k == 0:
            tup = self.nieokresl(editor, self.epoki)
            if self.fakty[w].set_epoka(tup[0],tup[1]):
                model.setItemData(index,{Qt.DisplayRole:tup[1]})
        elif k == 1:
            tup = self.nieokresl(editor, self.kultury)
            if self.fakty[w].set_kultura(tup[0],tup[1]):
                model.setItemData(index,{Qt.DisplayRole:tup[1]})    
        elif k == 2:
            tup = self.nieokresl(editor, self.funkcje)
            if self.fakty[w].set_funkcja(tup[0],tup[1]):
                model.setItemData(index,{Qt.DisplayRole:tup[1]})    
        elif k == 3:
            txt = unicode(editor.toPlainText())
            if self.fakty[w].set_wartosc("mas",txt):
                model.setItemData(index,{Qt.DisplayRole:txt}) 
        elif k == 4:
            txt = unicode(editor.toPlainText())
            if self.fakty[w].set_wartosc("wyod",txt):
                model.setItemData(index,{Qt.DisplayRole:txt})   
        elif k == 5:
            num = editor.value()
            if self.fakty[w].set_wartosc("cer",num):
                model.setItemData(index,{Qt.DisplayRole:num})
        elif k == 6:
            num = editor.value()
            if self.fakty[w].set_wartosc("kam",num):
                model.setItemData(index,{Qt.DisplayRole:num}) 
        elif k == 7:
            num = editor.value()
            if self.fakty[w].set_wartosc("met",num):
                model.setItemData(index,{Qt.DisplayRole:num})                        
            
    def set_slowniki(self,ep_slow,kul_slow,fun_slow):
        self.epoki = ep_slow
        self.kultury = kul_slow
        self.funkcje = fun_slow
           
            
    

class MaterialyTab(QWidget):
    
    zaznaczony = -1 # zaznaczony wiersz
    nowy = False
    def __init__(self,stan,dane,parent=None):
        QWidget.__init__(self,parent)
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.initTab(parent)
        self.edytor = FaktyEdytor(stan,dane,self)
        self.tabela.setItemDelegate(self.edytor)
        self.edytor.set_slowniki(dane.epoki(),dane.kultury(),dane.funkcje())
        self.fakty = dane.fakty(stan)
        self.dane = dane
        self.stan = stan
        for fakt in self.fakty:
            self.wstaw_fakt(fakt)
        self.connect(self.tabela,SIGNAL('itemChanged(QTableWidgetItem *)'),self.dodaj_wiersz_tab)
        
    def initTab(self,parent=None):
        self.tabela = QTableWidget(parent)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.vbox.addWidget(self.tabela)    
        self.tabela.setSortingEnabled(False)
        self.tabela.setRowCount(1)
        self.tabela.setItem(0,0,self.__item('<Nowy>'))
        self.tabela.setColumnCount(8)
        self.tabela.setHorizontalHeaderItem(0,self.__item("Epoka"))
        self.tabela.setHorizontalHeaderItem(1,self.__item("Kultura"))
        self.tabela.setHorizontalHeaderItem(2,self.__item("Funkcja"))
        self.tabela.setHorizontalHeaderItem(3,self.__item("Masowe"))
        self.tabela.setHorizontalHeaderItem(4,self.__item("Wydzielone"))
        self.tabela.setHorizontalHeaderItem(5,self.__item("Ceramika"))
        self.tabela.setHorizontalHeaderItem(6,self.__item("Kamienie"))
        self.tabela.setHorizontalHeaderItem(7,self.__item("Metale"))
        
    def __item(self,var):
        #print var
        #x = QApplication.translate(str(var), str(var), None,QApplication.UnicodeUTF8)
        if isinstance(var,unicode):
            return QTableWidgetItem(var)
        else:
            return QTableWidgetItem(QApplication.translate(unicode(var).encode('utf-8'), unicode(var).encode('utf-8'), None,QApplication.UnicodeUTF8))     
        
    def dodajWiersz(self,nowy_wiersz):
        tr = self.tabela.rowCount()
        for (wi,w) in enumerate(nowy_wiersz):
            #print w
            self.tabela.setItem(tr-1,wi,self.__item(w))
        self.tabela.insertRow(tr)    
        self.tabela.setItem(tr,0,self.__item('<Nowy>'))   
        self.tabela.resizeColumnsToContents()   
    
    
    def dodaj_wiersz_tab(self,item):
        tr = self.tabela.rowCount()
        if not self.nowy and item.row() == tr-1:
            self.nowy = True 
            self.tabela.insertRow(tr)
            self.tabela.setItem(tr,0,self.__item('<Nowy>')) 
        else:
            self.nowy = False
    
    def wstaw_fakt(self,fakt):
        self.dodajWiersz([fakt.epoka_nazwa,fakt.kultura_nazwa,fakt.funkcja_nazwa,fakt.mas,fakt.wyod,fakt.cer,fakt.kam,fakt.met])   
        self.edytor.dodajFakt(fakt)
            
    def zapisz(self):
        for fakt in self.edytor.fakty:
            if fakt.czy_nowy and fakt.czy_mod:
                print fakt.zapisz()
            elif fakt.czy_mod:
                print fakt.zapisz()