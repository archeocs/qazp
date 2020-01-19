# -*- coding: utf-8 -*-

# 20qazp
# (c) Milosz Piglas 2014 Wszystkie prawa zastrzezone

# Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
# 
#      * Redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above
#  copyright notice, this list of conditions and the following disclaimer
#  in the documentation and/or other materials provided with the
#  distribution.
#      * Neither the name of 20qazp nor the names of its
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

from PyQt5.QtCore import QObject, QVariant, Qt, QFile, QTextStream, QIODevice
from PyQt5.QtWidgets import QAction,QMessageBox,QInputDialog, QProgressDialog, QFileDialog, QDialog

from functools import partial
from locale import getpreferredencoding

from .filtred import FiltrWidget
from widok.lista import GTabModel2, GFrame
from dane.zrodla import gzdjecia, get_warstwa, szukaj_zdjecia,getPolaczenie2,\
    rejestr_map, stLista, sqlListaId
from widok.proped import conw, PropWidok, PropFrame
from lib.qgsop import usun, tempWarstwa, dodaj, dodajObj
from dane.model import ZDJECIA_LOTNICZE_ATR
from dane.gtypy import Punkt
from dane.tabela import *

def tab_model(obiekty,parent=None):
    return GTabModel2([('Ident','id'),('Folder','folder'),('Klatka','klatka') ,('Data','data_wykonania')],obiekty,parent)

class ListaZdjec(GFrame):

    def __init__(self, warstwa, lista, iface, win, parent=None):
        GFrame.__init__(self, win, lista, parent)
        self.setObjectName(u'Zdjęcia lotnicze')
        self.warstwa = warstwa
        self._if = iface
        self._win = win
        self._win.statusBar().showMessage("Wyszukano %s obiektow %s"%(str(self.warstwa.featureCount()),
               self.warstwa.dataProvider().dataSourceUri()))
        self._con = getPolaczenie2(self.warstwa)

    def akcja_wyswietl(self):
        atrs = self.warstwa.dataProvider().fields()
        nv = tempWarstwa(self.wszystkie(), "filtr_"+self.warstwa.name(), "Point", atrs)
        nv.setCrs(self.warstwa.crs())
        if rejestr_map().addMapLayer(nv):
            QMessageBox.information(self,'info','Do projektu zostala dodana warstwa '+nv.name())

    def utworz_model(self, gobs):
        return tab_model(gobs, self)

    def akcja_zmien(self):
        ww = self.wybrany_wiersz()[1]
        ed = edytor(self.warstwa, ww, self._win)
        self._win.dodaj(ed)

    def _akcjaDrukuj(self):
        pass

    def _anulujFiltr(self):
        self._win.usun()

    def _zastosujFiltr(self, mapa):
        self._win.usun()
        fzbior = None
        for (k, m) in mapa.items():
            rf = k.filtr(m)
            s = sqlListaId(self._con, rf[0], rf[1])
            if fzbior is None:
                fzbior = s
            else:
                fzbior &= s # przekroj zbiorow - interesujace sa tylko powtarzajace sie identyfikatory
        f = self.setFiltr(fzbior)
        QMessageBox.information(self,'Filtrowanie','Filtr zastosowany. Wybrano '+str(f))

    def _akcjaFiltruj(self):
        fw = FiltrWidget(self._con, tabele=[zdjeciaLotnicze(self._con)])
        fw.filtruj.connect(self._zastosujFiltr)
        fw.anuluj.connect(self._anulujFiltr)
        self._win.dodaj(fw)

    def akcja_usun(self):
        ww = self.wybrany_wiersz()
        odp = QMessageBox.question(self, u'Usuwanie stanowiska', u'Czy na pewno chcesz usunąć stanowisko %d'%ww[1]['id'].toInt()[0],
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if odp != QMessageBox.Yes:
            return
        if usun(self.warstwa, ww[1].feature()):
            self.getModel().removeRow(ww[0].row())
            self._win.statusBar().showMessage(u'Zdjęcie usunięte')

    def _akcjaOk(self):
        self._con.zakoncz()
        self._win.usun()

class WyszukajAkcja(QAction):

    def __init__(self,iface,window):
        QAction.__init__(self,'Wyszukaj',window)
        self.triggered.connect(self.wykonaj)
        self._win = window
        self._iface = iface

    def wykonaj(self):
        trasy = get_warstwa('zdjecia_lotnicze')
        if trasy is None:
            QMessageBox.warning(self._win,u'Wyszukaj',u'Przed wyszukiwaniem należy otworzyć warstwę "zdjecia_lotnicze"')
            return
        warunek = QInputDialog.getText(self._win, u'Zdjęcie', u'Wprowadź warunek', text="id > 0")
        if warunek[1]:
            warstwa = szukaj_zdjecia(str(warunek[0]))
            mf = ListaZdjec(warstwa,gzdjecia(warstwa),self._iface,self._win)
            self._win.dodaj(mf)

class ImportujAkcja(QAction):

    def __init__(self, iface, window):
        QAction.__init__(self, 'Importuj', window)
        self.triggered.connect(self.wykonaj)
        self._win = window
        self._iface = iface
        self.wykazy = {}
        self.prefEncoding = getpreferredencoding()

    def getWykaz(self, warstwa, wykNazwa, wartosc):
        if not wartosc:
            return None
        if wykNazwa not in self.wykazy:
            self.wykazy[wykNazwa] = {}
        upWartosc = wartosc.upper()
        if upWartosc in self.wykazy[wykNazwa]:
            return self.wykazy[wykNazwa][upWartosc]
        con = getPolaczenie2(warstwa)
        sql = 'select id from '+wykNazwa+' where nazwa = ?'
        ident = con.jeden(sql, [upWartosc])
        if ident:
            con.zakoncz()
            self.wykazy[wykNazwa][upWartosc] = ident[0]
            return ident[0]
        ident = con.getMax(wykNazwa) + 1
        con.wykonaj('insert into '+wykNazwa+' values (?, ?, ?)', [ident, upWartosc[:2], upWartosc], True)
        con.zakoncz()
        self.wykazy[wykNazwa][upWartosc] = ident
        return ident

    def czytajQt(self, plik):
        wiersze = []
        kolumny = ['folder', 'klatka', 'gDlugosc', 'gSzerokosc', 'miejscowosc', 'gmina',
                   'powiat', 'wojewodztwo', 'autor', 'pilot',
        'dataWykonania', 'czasWykonania','nosnik','prawaAutorskie', 'projekt', 'numer', 'zleceniodawca', 'platnik']
        ff = QFile(plik)
        ff.open(QIODevice.ReadOnly)
        stream = QTextStream(ff)
        line = stream.readLine()
        while not stream.atEnd():
            line = stream.readLine()
            wmapa = dict(zip(kolumny, str(line).split(";")))
            wiersze.append(wmapa)
        ff.close()
        return wiersze


    def wierszeNaZdjecia(self, wiersze):
        warstwa = get_warstwa('zdjecia_lotnicze')
        for w in wiersze:
            zdj = Zdjecie()
            zdj.folder, zdj.klatka = w['folder'], w['klatka']
            zdj.gDlugosc, zdj.gSzerokosc = w['gDlugosc'].replace(',','.'), w['gSzerokosc'].replace(',','.')
            zdj.dataWykonania, zdj.czasWykonania = w['dataWykonania'], w['czasWykonania']
            zdj.nosnik, zdj.prawaAutorskie = w['nosnik'][0], w['prawaAutorskie']

            zdj.miejscowosc = self.getWykaz(warstwa, 'miejscowosci', w['miejscowosc'])
            zdj.gmina = self.getWykaz(warstwa, 'gminy', w['gmina'])
            zdj.powiat = self.getWykaz(warstwa, 'powiaty', w['powiat'])
            zdj.wojewodztwo = self.getWykaz(warstwa, 'wojewodztwa', w['wojewodztwo'])

            zdj.projekt = self.getWykaz(warstwa, 'projekty', w['projekt'])
            zdj.zleceniodawca = self.getWykaz(warstwa, 'podmioty', w['zleceniodawca'])
            zdj.platnik = self.getWykaz(warstwa, 'podmioty', w['platnik'])
            zdj.autor = self.getWykaz(warstwa, 'podmioty', w['autor'])
            zdj.pilot = self.getWykaz(warstwa, 'podmioty', w['pilot'])
            zdj.numer = w['numer']
            yield zdj


    def wykonaj(self):
        warstwa = get_warstwa('zdjecia_lotnicze')
        if warstwa is None:
            QMessageBox.warning(self._win,u'Import Zdjęć',u'Przed importem należy otworzyć warstwę "zdjecia_lotnicze"')
            return
        fn = QFileDialog.getOpenFileName(self._win, filter='Dane CSV (*.csv)')
        if not fn:
            return
        wiersze = self.czytajQt(str(fn[0]))
        indeks = warstwa.maximumValue(0)
        if isinstance(indeks, QVariant) and not indeks.isNull():
            indeks = indeks.toInt()[0]
        elif isinstance(indeks, QVariant):
            indeks = 0
        warstwa.startEditing()
        postep = QProgressDialog(u'Dodaję zdjęcia', "Cancel", 0, len(wiersze)+1)
        postep.setWindowModality(Qt.WindowModal)
        sukces = False
        for (zi, z) in enumerate(self.wierszeNaZdjecia(wiersze)):
            postep.setValue(zi)
            postep.setLabelText(u'Zdjęcie %s/%s'%(z.folder, z.klatka))
            indeks += 1
            if not dodajObj(warstwa, indeks, z.mapa(), z.geom()):
                warstwa.rollBack()
                break
        else:
            sukces = warstwa.commitChanges()
        postep.setValue(len(wiersze)+1)
        if sukces:
            QMessageBox.information(self._win,u'Dodawanie zdjęć',u'Dodano %s zdjęć' % len(wiersze))
        else:
            msg = u'Zdjęcia nie zostały dodane\nBłędy:\n'
            msg += '\n'.join([str(s) for s in warstwa.commitErrors()])
            QMessageBox.information(self._win, u'Dodawanie zdjęć', msg)
            warstwa.rollBack()

def fdb(ident,war,tab):
    if ident is None:
        return None
    if isinstance(ident, QVariant):
        sid=str(ident.value())
    else:
        sid = str(ident)
    if sid is None or sid == '':
        return 'PUSTY'
    try:
        con = getPolaczenie2(war)
        ret = con.jeden('select nazwa from '+tab+' where id=?',[sid])
        con.zakoncz()
        if ret:
            return ret[0]
    except :
        return 'select nazwa from '+tab+' where id='+sid

def funkcja(warstwa, tabela):
    return partial(fdb, war=warstwa, tab=tabela)

class Zdjecie(object):

    def __init__(self):
        self.folder, self.klatka, self.dataWykonania, self.czasWykonania = None, None, None, None
        self.autor, self.pilot, self.miejscowosc, self.gmina = None, None, None, None
        self.powiat, self.wojewodztwo, self.projekt, self.numer = None, None, None, None
        self.zleceniodawca, self.platnik, self.prawaAutorskie, self.nosnik = None, None, None, None
        self.gSzerokosc = None
        self.gDlugosc = None

    def punkt(self):
        return Punkt(self.gDlugosc, self.gSzerokosc)

    def geom(self):
        return self.punkt().geom()

    def mapa(self):
        return {1:self.folder, 2:self.klatka,  3:self.miejscowosc, 4:self.gmina,
                5:self.powiat, 6:self.wojewodztwo,
                7:self.autor, 8:self.pilot, 9:self.dataWykonania, 10:self.czasWykonania,
                11:self.prawaAutorskie, 12:self.projekt, 13:self.numer,
                14:self.zleceniodawca, 15:self.platnik,  16:self.nosnik}


class ZdjecieEdytor(PropWidok):
    vrd = [('C',u'Cyfrowe'),('A',u'Analogowe')]
    wrd = partial(conw,slow=dict(vrd))
    def __init__(self,qgsWarstwa,dane=None,parent=None):
        PropWidok.__init__(self,parent)
        mdb = funkcja(qgsWarstwa,'miejscowosci')
        gdb = funkcja(qgsWarstwa, 'gminy')
        pdb = funkcja(qgsWarstwa, 'powiaty')
        wdb = funkcja(qgsWarstwa, 'wojewodztwa')
        fpodmioty = funkcja(qgsWarstwa, 'podmioty')
        fprojekty = funkcja(qgsWarstwa, 'projekty')
        opt = [(u'Folder', 'folder', self.nic),
               (u'Klatka', 'klatka', self.nic),
               (u'Data wykonania', 'data_wykonania', self.nic),
               (u'Czas wykonania', 'czas_wykonania', self.nic),
               (u'Autor', 'autor', fpodmioty),
               (u'Pilot', 'pilot', fpodmioty),
               (u'Miejscowość','miejscowosc',mdb), (u'Gmina','gmina',gdb), (u'Powiat','powiat',pdb),
               (u'Województwo' ,'wojewodztwo',wdb),
               (u'Projekt', 'projekt', fprojekty), (u'Numer', 'numer', self.nic),
               (u'Zleceniodawca', 'zleceniodawca', fpodmioty),
               (u'Płatnik', 'platnik', fpodmioty), (u'Prawa autorskie', 'prawa_autorskie', self.nic),
               (u'Nośnik', 'nosnik', self.wrd)]
        self.ustawModel(dane,opt)
        self.dodajOpt(15, self.vrd)
        self.dodajDb(4, (qgsWarstwa, 'podmioty')).dodajDb(5, (qgsWarstwa, 'podmioty'))\
            .dodajDb(10, (qgsWarstwa, 'projekty')).dodajDb(12, (qgsWarstwa, 'podmioty'))\
            .dodajDb(13, (qgsWarstwa, 'podmioty'))
        self.dodajDb(6,(qgsWarstwa,'miejscowosci')).dodajDb(7,(qgsWarstwa,'gminy'))\
            .dodajDb(8,(qgsWarstwa,'powiaty')).dodajDb(9,(qgsWarstwa,'wojewodztwa'))

def startEd(dane, win):
    warstwa = get_warstwa('zdjecia_lotnicze')
    return ZdjecieEdytor(warstwa, dane, win)

def edytor(warstwa, dane, win, parent=None):
    partEd = partial(ZdjecieEdytor, qgsWarstwa=warstwa)
    return PropFrame(warstwa, dane, win, ZDJECIA_LOTNICZE_ATR, startEd, parent)
