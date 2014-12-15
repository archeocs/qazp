# -*- coding: utf-8 -*-

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

import json
        
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QAction, QMessageBox, QFileDialog
from dane.zrodla import get_warstwa, getPolaczenie2
from lib.uzytki import dostosujSchemat, wykonajPolecenie

class SchematAkcja(QAction):
    def __init__(self,iface,window):
        QAction.__init__(self,'Dostosuj schemat',window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        warstwa = get_warstwa('stanowiska')
        if warstwa is None:
            QMessageBox.warning(self._win,u'Dostosuj schemat',u'Przed wyszukiwaniem należy otworzyć warstwę "stanowiska"')
            return 
        pytanie = QMessageBox.question(self._win, u'Dostosuj schemat', u'Czy została wykonana kopia zapasowa bazy?\n'\
                                       u'Czy na pewno chcesz zmodyfikować schemat bazy danych?', QMessageBox.Yes | QMessageBox.No, 
                                       QMessageBox.No)
        if pytanie == QMessageBox.Yes:
            con = getPolaczenie2(warstwa)
            if dostosujSchemat(con):
                self._win.statusBar().showMessage("Schemat zmieniony")
            else:
                self._win.statusBar().showMessage("Niepowodzenie")
            con.zakoncz()

class SkryptAkcja(QAction):
    def __init__(self,iface,window):
        QAction.__init__(self,'Wykonaj skrypt',window)
        #QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self.triggered.connect(self.wykonaj)
        self._win = window
        self._iface = iface
    
    def uruchomSkrypt(self, con, plik):

        f = open(plik)
        skrypt = json.load(f)
        for s in skrypt:
            if wykonajPolecenie(con, s['stmt']) != s['wynik']:
                con.wycofaj()
                f.close()
                return False
        con.zatwierdz()
        f.close()
        return True
        
    def wykonaj(self):
        warstwa = get_warstwa('stanowiska')
        if warstwa is None:
            QMessageBox.warning(self._win,u'Wykonaj skrypt',u'Przed wyszukiwaniem należy otworzyć warstwę "stanowiska"')
            return 
        fn = QFileDialog.getOpenFileName(self._win, filter='JSQL (*.jsql)')
        if fn is None or str(fn) == "":
            return
        pytanie = QMessageBox.question(self._win, u'Wykonaj skrypt', u'Czy została wykonana kopia zapasowa bazy?\n'\
                                       u'Czy na pewno chcesz wykonać skrypt?', QMessageBox.Yes | QMessageBox.No, 
                                       QMessageBox.No)
        if pytanie == QMessageBox.Yes:
            con = getPolaczenie2(warstwa)
            if self.uruchomSkrypt(con, str(fn)):
                self._win.statusBar().showMessage("Zmiany wprowadzone")
            else:
                self._win.statusBar().showMessage("Niepowodzenie")
            con.zakoncz()

class LogowanieAkcja(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,u'Rejestracja zdarzeń',window)
        self.triggered.connect(self.wykonaj)
        #QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        self.setCheckable(True)
    
    def wykonaj(self):
        import logging
        if self.isChecked():
            plik = QFileDialog.getSaveFileName(self._win, u'Proszę wybrać plik, w którym będą zapisywne zdarzenia')
            if plik:
                logging.basicConfig(filename=str(plik), level=logging.INFO)
        else:
            logging.shutdown()
            logging.shutdown()
            
class NaprawaAkcja(QAction):

    def __init__(self, iface, window):
        QAction.__init__(self, u'Napraw dane', window)
        self.triggered.connect(self.wykonaj)
        self._win = window
        self._iface = iface
    
    def _naJson(self, wiersz):
        mapa = {}
        for k in wiersz.keys():
            mapa[k] = wiersz[k]
        return json.dumps(mapa)
    
    def _wyszukajDuplikaty(self, tabela, polaczenie):
        sql = 'select stanowisko, count(*) from %s group by stanowisko having (count(*) > 1) order by stanowisko' % tabela
        dupSql = 'select s.obszar, s.nr_obszar, t.* from %s t join stanowiska s on t.stanowisko = s.id where stanowisko = ? order by s.obszar, s.nr_obszar' % tabela
        stanowiska = polaczenie.wszystkie(sql)
        polecenia = []
        for s in stanowiska:
            dr = polaczenie.wszystkie(dupSql, [s['stanowisko']])
            for r in dr[1:]:
                polecenia.append((self._naJson(r), 'delete from %s where id = %s and stanowisko = %s' % (tabela, r['id'], r['stanowisko']), r['obszar'], r['nr_obszar']))
        return polecenia
        
    def _usunDuplikaty(self, polecenia, polaczenie):
        fn = QFileDialog.getSaveFileName(self._win, filter='TXT (*.txt)')
        if fn is None or str(fn) == "":
            return
        fn = unicode(fn)
        if not fn.endswith('.txt'):
            fn += '.txt'
        with open(fn, 'w') as fout:
            for (tab, listaSql) in polecenia.iteritems():
                fout.write(tab)
                fout.write('\n-------------------------------------\n')
                for sql in listaSql:
                    fout.write('::: %s \ %s :::'%(sql[2],sql[3]))
                    fout.write(sql[0])
                    fout.write('\n')
        
        for (tab, listaSql) in polecenia.iteritems():
            print '----------------', tab, '------------------------'
            for sql in listaSql:
                x = polaczenie.wykonaj(sql[1], zatw = False)
                if x != 1:
                    return False
        return True
    
    def _duplikaty(self):
        listaDup = {}
        puste = True
        tabele = ['fizgeo_dane', 'ekspozycja_dane', 'obszar_dane', 'teren_dane', 'karty', 'aktualnosci', 'zagrozenia',
                    'wnioski', 'gleba_dane']
        warstwa = get_warstwa('stanowiska')
        if warstwa is None:
            QMessageBox.warning(self._win,u'Napraw dane',u'Przed wyszukiwaniem należy otworzyć warstwę "stanowiska"')
            return 
        polaczenie = getPolaczenie2(warstwa, True)
        for t in tabele:
            dt = self._wyszukajDuplikaty(t, polaczenie)
            if dt:
                listaDup[t] = dt
                puste = False
        if puste:
            QMessageBox.information(self._win, u'Napraw dane', u'Dane są poprawne', QMessageBox.Ok)
            return
        pytanie = QMessageBox.question(self._win, u'Napraw dane', u'Czy została wykonana kopia zapasowa bazy?\n'\
                                       u'Kliknij TAK aby naprawić dane', QMessageBox.Yes | QMessageBox.No, 
                                       QMessageBox.No)
        if pytanie == QMessageBox.Yes:
            zatwierdz = self._usunDuplikaty(listaDup, polaczenie)
            if zatwierdz:
                polaczenie.zatwierdz()
                QMessageBox.information(self._win, u'Napraw dane', u'SUKCES', QMessageBox.Ok)
            else:
                polaczenie.wycofaj()
                print 'FAIL'
            polaczenie.zakoncz()
                    
           
    def wykonaj(self):
        self._duplikaty()
