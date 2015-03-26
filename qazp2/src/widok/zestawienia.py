# -*- coding: utf-8 -*-

# (c) Milosz Piglas 2013-2014 Wszystkie prawa zastrzezone

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
from dane.tabela import WSZYSTKIE, stanowiska, Atrybut, Warunek, fakty, klasyfikacja
from dane.zrodla import get_warstwa, getPolaczenie2
from qtqube.qtqube import QtQube
from dbschemat import utworzSchemat
from functools import partial
from locale import strcoll

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

    def _sortujDane(self, arow=[], brow=[], sk=0):
        war = self._odtw.odtworz(sk, arow[sk])
        wbr = self._odtw.odtworz(sk, brow[sk])
        return strcoll(war, wbr)

    def sort(self, kolumna, porzadek=Qt.AscendingOrder):
        self.beginResetModel()
        self._dane.sort(partial(self._sortujDane, sk=kolumna))
        self.endResetModel()

    def data(self, indeks, rola=Qt.DisplayRole):
        r, c = indeks.row(), indeks.column()
        if rola == Qt.DisplayRole:
            return self._odtw.odtworz(c, self._dane[r][c])
        return None
        
    
class WynikWidget(QTableView):


    def __init__(self, odtwarzacz, dane, parent=None):
        QTableView.__init__(self, parent=parent)
        self.setModel(WidokZestModel(odtwarzacz, dane))
        #self.setSortingEnabled(True)
        header = self.horizontalHeader()
        header.sectionClicked.connect(self._sortuj)
        self._sortOrder = Qt.AscendingOrder
        self._altSortOrder = Qt.DescendingOrder

    def _sortuj(self, kolumna):
        self.sortByColumn(kolumna, self._sortOrder)
        so = self._sortOrder
        self._sortOrder = self._altSortOrder
        self._altSortOrder = so

    def zapisz(self, plik):
        f = open(plik, 'wb')
        model = self.model()
        cc = model.columnCount()
        head = u';'.join(
            [
                unicode(model.headerData(c, Qt.Horizontal)) 
                    for c in range(cc)
            ]
        )+u';\n'
        f.write(head.encode('utf-8'))
        rc = model.rowCount()
        for r in range(rc):
            row = u';'.join(
                [
                    unicode(model.data(model.index(r, c))) 
                        for c in range(cc)
                ]
            )+u';\n'
            f.write(row.encode('utf-8'))
        f.close()
        
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

class WynikZestFrame(QFrame):
    
    def __init__(self, win, dane, odtwarzacz, parent=None):
        QFrame.__init__(self, parent=parent)
        self._grid = QGridLayout(self)
        self._wgt = WynikWidget(odtwarzacz, dane, parent=self)
        self._grid.addWidget(self._wgt, 0, 0)
        self._grid.setRowMinimumHeight(0,150)
        self._grid.setColumnMinimumWidth(0,150)
        bb = QDialogButtonBox()
        self._grid.addWidget(bb, 1, 0)
        self._btnDrukuj = bb.addButton('Drukuj', QDialogButtonBox.ApplyRole)
        self._btnDrukuj.setObjectName('drukuj')
        self._btnCsv = bb.addButton('Zapisz', QDialogButtonBox.ApplyRole)
        self._btnCsv.setObjectName('zapisz')
        self._btnZamknij = bb.addButton('Zamknij', QDialogButtonBox.ApplyRole)
        self._btnZamknij.setObjectName('zamknij')
        self._win = win
        bb.clicked.connect(self._btnKlik)
   
    def _btnKlik(self, btn):
        on = str(btn.objectName())
        if on == 'zamknij':
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
            self._wgt.drukuj(dev)
        elif on == 'zapisz':
            plik = QFileDialog.getSaveFileName(parent=self, filter='CSV (*.csv)')
            self._wgt.zapisz(str(plik))
        else:
            print on
            
class ZestFrame(QFrame):
    
    def __init__(self, con, win, parent=None):
        QFrame.__init__(self, parent=parent)
        self._grid = QGridLayout(self)
        schemat = utworzSchemat()
        self._ed = QtQube(schemat, parent=self)
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
        self._btnCsv = bb.addButton('Zapisz', QDialogButtonBox.ApplyRole)
        self._btnCsv.setObjectName('zapisz')
        self._btnZamknij = bb.addButton('Zamknij', QDialogButtonBox.ApplyRole)
        self._btnZamknij.setObjectName('zamknij')
        self._btnWstecz.setVisible(False)
        self._btnDrukuj.setVisible(False)
        self._btnCsv.setVisible(False)
        self._con = con
        self._win = win
        bb.clicked.connect(self._btnKlik)
        self._tabzest = []
        self._tabzest.extend(WSZYSTKIE)
        self._tabzest.append(stanowiska(con))
        self._tabzest.append(klasyfikacja(con))
    
    def _konwertujAtrybut(self, qubeAtr):
        print 'konwertuje ', qubeAtr.view.source, qubeAtr.name
        widok = qubeAtr.view.source
        atr = qubeAtr.name
        for tabela in self._tabzest:
            if tabela.tnazwa == widok:
                for a in tabela.atrs:
                    if a.anazwa == atr:
                        return a
                print tabela.tnazwa, atr
                nowy = Atrybut(atr, etykieta=qubeAtr.realName())
                nowy.tabela = tabela
                return nowy
        raise Exception('Brak atrybutu')
            
        
    def _btnKlik(self, btn):
        on = str(btn.objectName())
        print on
        if on == 'dalej':
            qubeWynik = self._ed.getQuery()
            pobierane = [self._konwertujAtrybut(a) for a in qubeWynik.attributes]
            odtw = Odtwarzacz(pobierane)
            params = {}
            for (k, v) in qubeWynik.params.iteritems():
                params[k] = self._konwertujAtrybut(v)
            if params:
                pd = ParamDialog(params, self)
                if pd.exec_() == QDialog.Accepted:
                    print qubeWynik.statement
                    wynik = self._con.wszystkie(qubeWynik.statement, pd.daneParam)
                else:
                    return
            else:
                print qubeWynik.statement
                wynik = self._con.wszystkie(qubeWynik.statement)
            self._tv = WynikWidget(odtw, wynik)
            self._grid.removeWidget(self._ed)
            self._ed.setParent(None)
            self._grid.addWidget(self._tv, 0, 0)
            self._btnDalej.setVisible(False)
            self._btnWstecz.setVisible(True)
            self._btnDrukuj.setVisible(True)
            self._btnCsv.setVisible(True)
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
        elif on == 'zapisz':
            plik = QFileDialog.getSaveFileName(parent=self, filter='CSV (*.csv)')
            self._tv.zapisz(str(plik))
########## parametry dialog

class ParamFrame(QFrame):

    def __init__(self, atrybuty, parent=None):
        QFrame.__init__(self, parent=parent)
        self._atrs = atrybuty
        self._kolejnosc = []
        self._form = QFormLayout(self)
        self.setLayout(self._form)
        for (n, a) in atrybuty.iteritems():
            self._kolejnosc.append(n)
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
        dt = {}
        for (ai, a) in enumerate(self._kolejnosc):
            wgt = self._form.itemAt(ai, QFormLayout.FieldRole).widget()
            if self._atrs[a].dowolnaWartosc:
                dt[a] = (str(wgt.text()))
            else:
                dt[a] = (self._atrs[a].kodwar(wgt.currentIndex()))
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
        self.triggered.connect(self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        st = get_warstwa('stanowiska')
        if st is None:
            QMessageBox.warning(self._win,u'Wyszukaj',u'Przed wyszukiwaniem należy otworzyć warstwę "stanowiska"')
            return 
        nf = ZestFrame(getPolaczenie2(st), self._win)
        self._win.dodaj(nf)
        
class DefZestawienieAkcja(QAction):
    
    def __init__(self, etykieta, iface, window, sql, fkols, fparams=None):
        QAction.__init__(self, etykieta, window)
        self.triggered.connect(self.wykonaj)
        self._win = window
        self._iface = iface
        self._pa = fparams
        self._sql = sql
        self._kols = fkols
        
    def wykonaj(self):
        st = get_warstwa('stanowiska')
        if st is None:
            QMessageBox.warning(self._win,u'Zestawienie',u'Przed wykonaniem zestawienia należy otworzyć warstwę "stanowiska"')
            return 
        con = getPolaczenie2(st)
        if self._pa:
            pd = ParamDialog(self._pa(con), self._win)
            if pd.exec_() == QDialog.Accepted:
                wynik = con.wszystkie(self._sql, pd.daneParam)
            else:
                return
        else:
            wynik = con.wszystkie(self._sql)
        self._win.dodaj(WynikZestFrame(self._win, wynik, Odtwarzacz(self._kols(con))))

def _klasyfikacja(iface, window, etykieta, warunek=None, atr_indeks=-1):
    sql = """ select S.obszar, S.nr_obszar, S.miejscowosc, S.nr_miejscowosc, S.data, S.rodzaj_badan, 
        jeda||'#'||coalesce(jedb,'')||'#'||coalesce(jed_relacja,'')||'#'||coalesce(jed_pewnosc,'') as jednostka,
        okresa||'#'||coalesce(okresb,'')||'#'||coalesce(okr_relacja,'')||'#'||coalesce(okr_pewnosc,'') as okres,
        funkcja||'###'||coalesce(fun_pewnosc,'') as fun, 
        masowy,wydzielony
        from stanowiska S join fakty F on S.id = F.stanowisko 
        where data  like :param0||'%' """ #AND """+warunek
    def parametry(con):
        if atr_indeks >= 0:
            fk = fakty(con)
            #st = stanowiska(con)
            return {'param0':Atrybut('data', etykieta=u'Rok/data badań'), 
                        'param1':fk.atrs[atr_indeks]}
        else:
            return {'param0':Atrybut('data', etykieta=u'Rok/data badań')}
        
    def kolumny(con):
        fk = fakty(con)
        st = stanowiska(con)
        return [st.atrs[0], st.atrs[1],  st.atrs[2], st.atrs[3], 
                Atrybut('data', etykieta=u'Data badań'), st.atrs[5],
                fk.atrs[0], fk.atrs[1], fk.atrs[2], 
                Atrybut('masowy', etykieta=u'Materiał masowy'),
                Atrybut('masowy', etykieta=u'Materiał wyodrębniony')]
    if warunek is not None:
        return DefZestawienieAkcja(etykieta, iface, window, sql+warunek, kolumny, parametry)
    else:
        return DefZestawienieAkcja(etykieta, iface, window, sql, kolumny, parametry)

def klasyfikacjaJednostka(iface, window):
    return _klasyfikacja(iface, window, 'Klasyfikacja kuluturowa wg jednostki', 
            ' AND :param1 in (jeda, jedb)', 0)

def klasyfikacjaOkres(iface, window):
    return _klasyfikacja(iface, window, 'Klasyfikacja kuluturowa wg okresu',
            ' AND :param1 in (okresa, okresb)', 1)

def klasyfikacjaData(iface, window):
    return _klasyfikacja(iface, window, u'Klasyfikacja kulturowa wg daty badań')
            
def jednostkiObszar(iface, window):
    sql = """select count(*) as LICZ, s.obszar, j.jednostka from stanowiska s join 
            (select distinct stanowisko, 
                jeda||'#'||coalesce(jedb,'')||'#'||coalesce(jed_relacja,'')||'#'||coalesce(jed_pewnosc,'') as jednostka 
            from fakty where jednostka is not null) j on s.id = j.stanowisko 
            group by s.obszar, j.jednostka"""
    def kolumny(con):
        return [Atrybut('count(*)', etykieta='LICZ()'), stanowiska(con).atrs[0], fakty(con).atrs[0]]
    return DefZestawienieAkcja('Jednostka, obszar', iface, window, sql, kolumny)

def jedOkrObszar(iface, window):
    sql = """SELECT count(*), H.obszar, I.jednostka,I.okres FROM stanowiska H join  
                (select distinct stanowisko, 
                    jeda||'#'||coalesce(jedb,'')||'#'||coalesce(jed_relacja,'')||'#'||coalesce(jed_pewnosc,'') as jednostka, 
                    okresa||'#'||coalesce(okresb,'')||'#'||coalesce(okr_relacja,'')||'#'||coalesce(okr_pewnosc,'') as okres 
                from fakty where jednostka is not null OR okres is not null) I on I.stanowisko = H.id 
                GROUP BY H.obszar, I.jednostka, I.okres"""
    def kolumny(con):
        f = fakty(con)
        return [Atrybut('count(*)', etykieta='LICZ()'), stanowiska(con).atrs[0], f.atrs[0], f.atrs[1]]
    return DefZestawienieAkcja('Jednostka, okres, obszar', iface, window, sql, kolumny)

def jedOkrFunObszar(iface, window):
    sql = """SELECT count(*), H.obszar, I.jednostka,I.okres,I.fun FROM stanowiska H join  
                (select distinct stanowisko, 
                        jeda||'#'||coalesce(jedb,'')||'#'||coalesce(jed_relacja,'')||'#'||coalesce(jed_pewnosc,'') as jednostka, 
                        okresa||'#'||coalesce(okresb,'')||'#'||coalesce(okr_relacja,'')||'#'||coalesce(okr_pewnosc,'') as okres, 
                        funkcja||'###'||coalesce(fun_pewnosc,'') as fun
                        from 
                    fakty where jednostka is not null OR okres is not null or fun is not null) I on I.stanowisko = H.id 
                    GROUP BY H.obszar, I.jednostka,I.okres,I.fun"""
    def kolumny(con):
        f = fakty(con)
        return [Atrybut('count(*)', etykieta='LICZ()'), stanowiska(con).atrs[0], f.atrs[0], f.atrs[1],f.atrs[2]]
    return DefZestawienieAkcja('Jednostka, okres, funkcja, obszar', iface, window, sql, kolumny)

def jednostkiMiej(iface, window):
    sql = """select count(*) as LICZ, s.miejscowosc, j.jednostka from stanowiska s join 
            (select distinct stanowisko, 
                jeda||'#'||coalesce(jedb,'')||'#'||coalesce(jed_relacja,'')||'#'||coalesce(jed_pewnosc,'') as jednostka 
            from fakty where jednostka is not null) j on s.id = j.stanowisko 
            group by s.miejscowosc, j.jednostka"""
    def kolumny(con):
        return [Atrybut('count(*)', etykieta='LICZ()'), stanowiska(con).atrs[2], fakty(con).atrs[0]]
    return DefZestawienieAkcja('Jednostka, miejscowosc', iface, window, sql, kolumny)

def jedOkrMiej(iface, window):
    sql = """SELECT count(*), H.miejscowosc, I.jednostka,I.okres FROM stanowiska H join  
                (select distinct stanowisko, 
                    jeda||'#'||coalesce(jedb,'')||'#'||coalesce(jed_relacja,'')||'#'||coalesce(jed_pewnosc,'') as jednostka, 
                    okresa||'#'||coalesce(okresb,'')||'#'||coalesce(okr_relacja,'')||'#'||coalesce(okr_pewnosc,'') as okres
                from fakty where jednostka is not null OR okres is not null) I on I.stanowisko = H.id 
                GROUP BY H.miejscowosc, I.jednostka, I.okres"""
    def kolumny(con):
        f = fakty(con)
        return [Atrybut('count(*)', etykieta='LICZ()'), stanowiska(con).atrs[2], f.atrs[0], f.atrs[1]]
    return DefZestawienieAkcja('Jednostka, okres, miejscowosc', iface, window, sql, kolumny)

def jedOkrFunMiej(iface, window):
    sql = """SELECT count(*), H.miejscowosc, I.jednostka,I.okres,I.fun FROM stanowiska H join  
                (select distinct stanowisko, 
                        jeda||'#'||coalesce(jedb,'')||'#'||coalesce(jed_relacja,'')||'#'||coalesce(jed_pewnosc,'') as jednostka, 
                        okresa||'#'||coalesce(okresb,'')||'#'||coalesce(okr_relacja,'')||'#'||coalesce(okr_pewnosc,'') as okres, 
                        funkcja||'###'||coalesce(fun_pewnosc,'') as fun
                        from 
                    fakty where jednostka is not null OR okres is not null or fun is not null) I on I.stanowisko = H.id 
                    GROUP BY H.miejscowosc, I.jednostka,I.okres,I.fun"""
    def kolumny(con):
        f = fakty(con)
        return [Atrybut('count(*)', etykieta='LICZ()'), stanowiska(con).atrs[2], f.atrs[0], f.atrs[1], f.atrs[2]]
    return DefZestawienieAkcja('Jednostka, okres, funkcja, miejscowosc', iface, window, sql, kolumny)            
