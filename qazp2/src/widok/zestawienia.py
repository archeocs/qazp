# -*- coding: utf-8 -*-

# (c) Milosz Piglas 2013 Wszystkie prawa zastrzezone

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

from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from PyQt4.QtGui import QItemEditorFactory, QStyledItemDelegate, QDialog, QVBoxLayout,\
                        QFormLayout, QComboBox, QLineEdit, QTableView, QWidget,\
                        QAbstractItemView, QHeaderView, QFontMetrics, QTextFormat,\
                        QPrinter, QTextTableFormat, QTextLength, QFont, QGridLayout,\
                        QFrame, QAction, QDialogButtonBox, QTextCursor, QTextDocument,\
                        QPlainTextEdit, QMessageBox, QFileDialog
from dane.tabela import SqlGenerator, WSZYSTKIE, stanowiska, Atrybut, Warunek
from dane.zrodla import get_warstwa, getPolaczenie2

############## Wyswietlanie wynikow zestawien ##################
class Odtwarzacz(object):

    def __init__(self, atrs): 
        self._atrs = atrs
    
    def liczbaAtrybutow(self):
        return len(self._atrs)
        
    def etykieta(self, i): # uzyta do wyswietlania naglowka
        return self._atrs[i].toStr()
        
    def odtworz(self, i, wartosc):
        if wartosc is None:
            return ""
        if self._atrs[i].dowolnaWartosc:
            return unicode(wartosc)
        return self._atrs[i].odtworz(wartosc)
        
class WidokZestModel(QAbstractTableModel):

    def __init__(self, odtwarzacz, dane=[]): # dane - wartosci pobrane z bazy
        QAbstractTableModel.__init__(self)
        self._dane = dane
        self._odtw = odtwarzacz
        
    def rowCount(self, model=QModelIndex()):
        return len(self._dane)
        
    def columnCount(self, model=QModelIndex()):
        return self._odtw.liczbaAtrybutow()
    
    def headerData(self, sekcja, orientacja, rola=Qt.DisplayRole):
        if orientacja == Qt.Horizontal and rola == Qt.DisplayRole:
            h = self._odtw.etykieta(sekcja)
            return h
        return None         
        
    def data(self, indeks, rola=Qt.DisplayRole):
        r, c = indeks.row(), indeks.column()
        if rola == Qt.DisplayRole:
            return self._odtw.odtworz(c, self._dane[r][c])
        return QVariant()
    
##### Edytor SQL - Tabela

class TypTablica(object):

    def __init__(self):
        self._tab = []
        self._typyKol = []
        self._wc = 0
        self._kc = 0
            
    def liczbaKolumn(self):
        return self._kc
        
    def liczbaWierszy(self):
        return self._wc
    
    def wiersze(self):
        for wt in self._tab:
            yield wt
        
    def dodajWiersze(self, ile=1):
        if ile < 1:
            raise Exception("liczba wierszy musi byc wieksza od 0")
        for i in range(ile):
            self._tab.append([None] * self._kc)
        self._wc += ile
        
    def dodajKolumne(self, typ): # grupa, typ
        pk = -1
        znaleziony = False
        for (ti, t) in enumerate(self._typyKol):
            if t == typ:
                znaleziony = True
            elif znaleziony:
                pk = ti
                break
        if pk >= 0:
            for wt in self._tab:
                wt.insert(pk, None)
            self._typyKol.insert(pk, typ)
        else:
            for wt in self._tab:
                wt.append(None)
            self._typyKol.append(typ)
        self._kc += 1
    
    def typ(self, k):
        return self._typyKol[k]
    
    def typyWar(self):
        for t in self._typyKol:
            yield t
        
    def wartosc(self, w, k):
        return self._tab[w][k]
        
    def setWartosc(self, wartosc, w, k):
        self._tab[w][k] = wartosc
        
    def kolumnyTyp(self, typ):
        return [x for x in range(len(self._typyKol)) if self._typyKol[x] == typ]
        
class TablicaModel(QAbstractTableModel):
    
    def __init__(self, tablica=TypTablica()):
        QAbstractTableModel.__init__(self)
        self._tab = tablica
        self._naglowki = ['Funkcja', 'Grupuj', 'Warunek']
        self._typy = ['funkcja', 'grupuj', 'warunek']
        
    def rowCount(self, model):
        return self._tab.liczbaWierszy()
        
    def columnCount(self, model):
        return self._tab.liczbaKolumn()
        
    def data(self, indeks, rola=Qt.DisplayRole): # wartosciami pol sa pary (tabela.Tabela, tabela.Atrybut)
        r, c = indeks.row(), indeks.column()
        if rola == Qt.DisplayRole:
            p = self._tab.wartosc(r, c)
            if p is not None:
                return p.toStr()
        elif rola == Qt.EditRole:
            return self._tab.wartosc(r, c)
        return QVariant()
        
    def setData(self, indeks, wartosc, rola=Qt.EditRole):
        #print 'W', wartosc[1].aetykieta
        r, c = indeks.row(), indeks.column()
        ct = self._tab.typ(c)
        kc = self._tab.liczbaKolumn()
        if ct == self._typy[2] and c == kc-1:
            self.beginResetModel()
            self._tab.dodajKolumne(self._typy[2])
            self.endResetModel()
        wc = self._tab.liczbaWierszy()
        if r == wc-1:
            self.beginResetModel()
            #print 'nowy wiersz'
            self._tab.dodajWiersze()
            self.endResetModel()
        self._tab.setWartosc(wartosc, r, c)
        self.dataChanged.emit(indeks, indeks)

    def flags(self,indeks):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable
        
class AtrybutyDelegate(QStyledItemDelegate):

    def __init__(self, atrybuty, parent=None):
        QStyledItemDelegate.__init__(self, parent=parent)
        self.setItemEditorFactory(QItemEditorFactory.defaultFactory())
        self._atrs = atrybuty
        
    def createEditor(self, parent, styl, indeks):
        self.initStyleOption(styl, indeks)
        print 'ok'
        cb = QComboBox(parent)
        for a in self._atrs: # atrybuty 
            cb.addItem(a.toStr())
        return cb
        
    def setEditorData(self, edytor, indeks):
        wartosc = indeks.data()
        for (ai, a) in enumerate(self._atrs):
            if a == wartosc:
                edytor.setCurrentIndex(ai)
                return
        edytor.setCurrentIndex(0)
    
    def setModelData(self, edytor, model, indeks):
        #print 'SET ', self._atrs[edytor.currentIndex()][1].aetykieta
        model.setData(indeks, self._atrs[edytor.currentIndex()])

################ Edytor SQL - ramka

class EWidget(QWidget):
    
    def __init__(self, con=None, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setLayout(QVBoxLayout(self))
        widok = QTableView()
        self.layout().addWidget(widok)
        self._typyTab = TypTablica()
        self._typyTab.dodajWiersze()
        self._typyTab.dodajKolumne('funkcja')
        self._typyTab.dodajKolumne('grupuj')
        self._typyTab.dodajKolumne('warunek')
        self._sqlGen = SqlGenerator()
        widok.setEditTriggers(QAbstractItemView.DoubleClicked)
        model = TablicaModel(self._typyTab)
        model.dataChanged.connect(self._zmianaWartosci)
        widok.setModel(model)
        #funatr = [(None, Atrybut('licz', etykieta='LICZ()'))]
        widok.setItemDelegateForColumn(0, AtrybutyDelegate([Atrybut('count(*)', etykieta='LICZ()')], parent=widok))
        tabPola = []
        for tab in WSZYSTKIE:
            tabPola.extend(tab.atrs)
            #for atr in tab.atrs:
            #    tabPola.append((tab, atr))
        if con is not None:
            tabPola.extend(stanowiska(con))
        widok.setItemDelegate(AtrybutyDelegate(tabPola, parent=widok))
        widok.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        
        self._podglad = QPlainTextEdit()
        self._podglad.setFixedHeight(5 * QFontMetrics(self._podglad.font()).lineSpacing())
        self.layout().addWidget(self._podglad)
        
    def _zmianaWartosci(self, start, koniec):
        r, c = start.row(), start.column()
        p = self._typyTab.wartosc(r, c)
        if c == 0:
            self._sqlGen.funkcje[r] = p
        elif c == 1:
            self._sqlGen.grupy[r] = p
        elif c > 1:
            self._sqlGen.warunki[r] = self._sqlGen.warunki.get(r, Warunek()).dodaj(p, c-2)
        if self._sqlGen.poprawny:
            self._podglad.setPlainText(unicode(self._sqlGen))
            
    @property
    def polecenie(self):
        if self._sqlGen.poprawny:
            return unicode(self._sqlGen)
        else:
            raise Exception('Niepoprawne polecenie')
            
    @property
    def poprawny(self):
        return self._sqlGen.poprawny
        
    @property
    def parametry(self):
        return self._sqlGen.params
        
    @property
    def pobierane(self):
        return self._sqlGen.pobierane
    
class WynikWidget(QTableView):

    def __init__(self, odtwarzacz, dane):
        QTableView.__init__(self)
        self.setModel(WidokZestModel(odtwarzacz, dane))
        
    def drukuj(self, drukarka):
        doc = QTextDocument()
        cur = QTextCursor(doc)
        model = self.model()
        rc, cc = model.rowCount(), model.columnCount()
        tfmt = QTextTableFormat()
        tfmt.setPageBreakPolicy(QTextFormat.PageBreak_AlwaysAfter)
        tfmt.setWidth(QTextLength(QTextLength.PercentageLength,100))
        tfmt.setCellPadding(2)
        tfmt.setBorderStyle(QTextTableFormat.BorderStyle_Solid)
        tab = cur.insertTable(rc+1, cc, tfmt) 
        # wstawienie naglowka
        BOLD = QFont('Times', 10, QFont.DemiBold)
        for c in range(cc):
            kom = tab.cellAt(0, c)
            kfmt = kom.format()
            kfmt.setFont(BOLD)
            kom.setFormat(kfmt)
            kom.firstCursorPosition().insertText(model.headerData(c, Qt.Horizontal))
        # wyniki zestawienia
        NORM = QFont('Times', 10, QFont.Normal)
        for r in range(rc):
            for c in range(cc):
                kom = tab.cellAt(r+1, c)
                kfmt = kom.format()
                kfmt.setFont(NORM)
                kom.setFormat(kfmt)
                kom.firstCursorPosition().insertText(model.data(model.index(r, c)))
        doc.print_(drukarka)
            
class ZestFrame(QFrame):
    
    def __init__(self, con, win, parent=None):
        QFrame.__init__(self, parent=parent)
        self._grid = QGridLayout(self)
        self._ed = EWidget(con, parent=self)
        self._grid.addWidget(self._ed, 0, 0)
        self._grid.setRowMinimumHeight(0,150)
        self._grid.setColumnMinimumWidth(0,150)
        bb = QDialogButtonBox()
        self._grid.addWidget(bb, 1, 0)
        self._btnDalej = bb.addButton('Dalej', QDialogButtonBox.ApplyRole)
        self._btnDalej.setObjectName('dalej')
        self._btnWstecz = bb.addButton('Wstecz', QDialogButtonBox.ApplyRole)
        self._btnWstecz.setObjectName('wstecz')
        self._btnDrukuj = bb.addButton('Drukuj', QDialogButtonBox.ApplyRole)
        self._btnDrukuj.setObjectName('drukuj')
        self._btnZamknij = bb.addButton('Zamknij', QDialogButtonBox.ApplyRole)
        self._btnZamknij.setObjectName('zamknij')
        self._btnWstecz.setVisible(False)
        self._btnDrukuj.setVisible(False)
        self._con = con
        self._win = win
        bb.clicked.connect(self._btnKlik)
        
    def _btnKlik(self, btn):
        on = str(btn.objectName())
        print on
        if on == 'dalej':
            if self._ed.poprawny:
                #print self._ed.pobierane
                odtw = Odtwarzacz(self._ed.pobierane)
                params = self._ed.parametry
                if params:
                    pd = ParamDialog(params, self)
                    if pd.exec_() == QDialog.Accepted:
                        wynik = self._con.wszystkie(self._ed.polecenie, pd.daneParam)
                    else:
                        return
                else:
                    wynik = self._con.wszystkie(self._ed.polecenie)
                self._tv = WynikWidget(odtw, wynik)
                self._grid.removeWidget(self._ed)
                self._ed.setParent(None)
                self._grid.addWidget(self._tv, 0, 0)
                self._btnDalej.setVisible(False)
                self._btnWstecz.setVisible(True)
                self._btnDrukuj.setVisible(True)
        elif on == 'wstecz':
            #biez = self._grid.itemAtPosition(0, 0).widget()
            self._grid.removeWidget(self._tv)
            self._tv.setParent(None)
            self._tv = None
            self._grid.addWidget(self._ed, 0, 0)
            self._btnDalej.setVisible(True)
            self._btnWstecz.setVisible(False)
            self._btnDrukuj.setVisible(False)  
        elif on == 'zamknij':
            biez = self._grid.itemAtPosition(0, 0).widget()
            biez.setParent(None)
            del biez
            self._win.usun(self)
        elif on == 'drukuj':
            plik = QFileDialog.getSaveFileName(parent=self, filter='PDF (*.pdf)')
            dev = QPrinter()
            dev.setOutputFormat(QPrinter.PdfFormat)
            dev.setOrientation(QPrinter.Portrait)
            dev.setOutputFileName(plik)
            self._tv.drukuj(dev)    
########## parametry dialog

class ParamFrame(QFrame):

    def __init__(self, atrybuty, parent=None):
        QFrame.__init__(self, parent=parent)
        self._atrs = atrybuty
        self._form = QFormLayout(self)
        self.setLayout(self._form)
        for a in atrybuty:
            if a.dowolnaWartosc:
                self._form.addRow(a.toStr(), QLineEdit())
            else:
                self._form.addRow(a.toStr(), self._combo(a.dozwolone)) 
                   
    def _combo(self, wartosci):
        c = QComboBox()
        for w in wartosci:
            c.addItem(w)
        return c
    
    @property    
    def dane(self):
        dt = []
        for (ai, a) in enumerate(self._atrs):
            wgt = self._form.itemAt(ai, QFormLayout.FieldRole).widget()
            if a.dowolnaWartosc:
                dt.append(str(wgt.text()))
            else:
                dt.append(a.kodwar(wgt.currentIndex()))
        return dt
        
class ParamDialog(QDialog):
    
    def __init__(self, atrybuty, parent=None):
        QDialog.__init__(self, parent=parent)
        box = QVBoxLayout(self)
        self.setLayout(box)
        self._pf = ParamFrame(atrybuty)
        box.addWidget(self._pf)
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.addWidget(bb)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        
    @property
    def daneParam(self):
        return self._pf.dane
    
class NoweZestawienieAkcja(QAction):
    
    def __init__(self, iface, window):
        QAction.__init__(self,u'Nowe zestawienie',window)
        self.triggered.connect(self.wykonaj())
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        st = get_warstwa('stanowiska')
        if st is None:
            QMessageBox.warning(self._win,u'Wyszukaj',u'Przed wyszukiwaniem należy otworzyć warstwę "stanowiska"')
            return 
        nf = ZestFrame(getPolaczenie2(st), self._win)
        self._win.dodaj(nf)