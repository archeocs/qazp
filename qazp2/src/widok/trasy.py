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

from PyQt5.QtCore import QVariant, QObject, Qt,QSize
from PyQt5.QtWidgets import QDialog, QVBoxLayout,QWidget,QFormLayout,QLineEdit,QDialogButtonBox,QMessageBox
from PyQt5.QtWidgets import QAction,QFileDialog,QInputDialog, QTableWidget, QTableWidgetItem,QComboBox,QLabel
from .lista import GTabModel,GFrame
from dane.zrodla import rejestr_map, get_warstwa, gtrasy, szukaj_trasy
from lib.gps import GpxPunktyLista,distr, TrackPoints
from lib.qgsop import usun, zmien,dodaj
from widok.proped import PropWidok, conw, PropFrame
from functools import partial
from dane.model import TRASY_ATR


def tab_model(obiekty,parent=None):
    return GTabModel(['Ident','Rodzaj','Data','Autor','Start','Koniec','Czest.','Uwagi'],obiekty,parent)

def txt(v,trim=False,mx=-1):
    if isinstance(v, QVariant):
        u = str(v.value())
    else:
        u = str(v)
    if trim:
        u = u.strip()
    if mx > 0:
        u = u[:mx]
    return u

class TrasyWidokEd(PropWidok):
    
    vrd = [('P',u'Powierzchniowe'),('W',u'Weryfikacja'),('L',u'Lotnicze')]
    wrd = partial(conw,slow=dict(vrd))
    def __init__(self,dane,parent=None):
        PropWidok.__init__(self,parent)
        opt=[(u'Rodzaj','rodzaj_badan',self.wrd),('Data','data',self.nic),
             (u'Autor','autor',self.nic),(u'Uwagi','uwagi',self.nic)]
        self.ustawModel(dane,opt)
        self.dodajOpt(0, self.vrd)

class TrasyFrame(GFrame):
    
    warstwa = None
    def __init__(self,warstwa,iface,win,parent=None):
        GFrame.__init__(self,win,gtrasy(warstwa))
        self.warstwa = warstwa
        self._if = iface
        self._win = win
        self._win.statusBar().showMessage("Wyszukano %s obiektow %s"%(str(self.warstwa.featureCount()),
                                                                      self.warstwa.dataProvider().dataSourceUri()))
        
    def utworz_model(self, gobs):
        return tab_model(gobs, self)
    
    def akcja_ok(self):
        QMessageBox.information(self, 'akcja_ok', 'OK')
        self.setVisible(False)
        
    def akcja_anul(self):
        self.setVisible(False)
        
    def akcja_wyswietl(self):
        if self.warstwa is not None:
            rejestr_map().addMapLayer(self.warstwa)
            QMessageBox.information(self,'info','Do projektu zostala dodana warstwa '+self.warstwa.name())
        
    def akcja_zmien(self):
        ww = self.wybrany_wiersz()[1]
        self._win.dodaj(PropFrame(self.warstwa,ww,self._win,TRASY_ATR,TrasyWidokEd))
                
    def akcja_usun(self):
        ww = self.wybrany_wiersz()[1]
        odp = QMessageBox.question(self, u'Usuwanie trasy', 
                u'Czy na pewno chcesz usunąć stanowisko wybraną trasę?',
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if odp != QMessageBox.Yes:
            return
        u = usun(self.warstwa,ww.feature())
        if u:
            QMessageBox.information(self, u'Usuwanie trasy', u'Trasa została usunięta')
            self.odswiez(gtrasy(self.warstwa))

def get_val_text(txt_fld):
    return str(txt_fld.text())

def get_val_combo(combo):
    return str(combo.currentText())

def get_index_combo(combo):
    return combo.currentIndex()
            
class TableGpsTracks(QTableWidget):
    
    def __init__(self,segments,parent=None):
        QTableWidget.__init__(self,parent)
        self.tracks = []
        self.segments = segments
        self.cov, self.mean = 0.0, 0.0
        self._handler_cov = None
        self.init_tab()
        
    def add_row(self,row):
        rindex = self.rowCount()
        self.insertRow(rindex)
        for (fi,f) in enumerate(row):
            if isinstance(f, bool):
                wit = QTableWidgetItem()
                wit.setData(Qt.CheckStateRole,Qt.Checked)
            else:
                wit = QTableWidgetItem(str(f))
            wit.setToolTip(str(f))
            #wit.sets
            self.setItem(rindex,fi,wit)     
    
    def get_selected(self):
        sel_rows = []
        for r in range(self.rowCount()):
            if self.item(r, 0).data(Qt.CheckStateRole) == Qt.Checked:
                sel_rows.append(r)
        return sel_rows
        
    def init_tab(self):
        self.setWordWrap(True)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([u'Dodaj', u'Data rozpoczęcia', u'Data zakończenia',u'Pierwszy punkt',
                                        u'Ostatni punkt',u'Liczba punktów'])   
        self.con_list = GpxPunktyLista()
       # if self.con_list.zlicz() > 0:
        for s in self.segments:
            self.add_row([True,s.min_czas(),s.max_czas(),s.pierw().wkt(),s.ost().wkt(),s.zlicz()]) 
            self.con_list += s
        d = distr(self.con_list.czas_delty())
        self.cov = round(d[1] / d[0],2)# / d[0]
        self.mean = round(d[0],2)
        self.resizeColumnsToContents()
        self.itemClicked.connect(self._update_cov)
    
    def set_meanhandler(self,h):
        self._handler_mean = h
        
    def _update_cov(self,it):
        if it.column() == 0:
            self.con_list = GpxPunktyLista()
            for s in self.get_selected():
                self.con_list += self.segments[s]
            d = distr(self.con_list.czas_delty())
            self.cov = round(d[1] / d[0],2)
            self.mean = round(d[0],2)
            if self._handler_mean:
                self._handler_mean(self.mean,self.cov)
            
class FormInfo(QWidget):
    
    def __init__(self,parent=None,info={},flds=[]):
        QWidget.__init__(self,parent)
        self.form = QFormLayout(self)
        self.info = info
        self._ff = flds
        
    def add_txt_field(self,key,lb):
        fld = QLineEdit() 
        if key in self.info:
            fld.setText(self.info[key])
        self.form.addRow(self._ff[lb], fld)
        return fld
    
    def add_combo_field(self,lb,values=[u'Wybierz'],ch=0):
        combo = QComboBox()
        combo.addItems(values)
        if ch < len(values):
            combo.setCurrentIndex(ch)
        else:
            combo.setCurrentIndex(0)
        self.form.addRow(self._ff[lb], combo)
        return combo
        
    def init_form(self):
        pass
            
class FormTracks(FormInfo):
    
    def __init__(self,parent=None,info={}):
        FormInfo.__init__(self,parent,info,[u'Data pomiarów', u'Autor', u'Rodzaj badań', 
                                            u'Częstotliwość odczytu', u'Uwagi',u'Współczynnik zmienności'])
        self.init_form()
        
    def init_form(self):
        self.data_txt = self.add_txt_field('data',0)
        self.data_txt.setInputMask('0000-00-00')
        self.autor_txt = self.add_txt_field('autor', 1)
        self.rodzaj_cmb = self.add_combo_field(2,[u'Nieokreślony',u'Lot',u'Powierzchniowe',u'Weryfikacja'], 0)
        self.czest_txt = self.add_txt_field('czest', 3)
        self.rozpr_txt = self.add_txt_field('rozpr', 5)
        self.rozpr_txt.setReadOnly(True)
        self.czest_txt.setInputMask('000')
        self.uwagi_txt = self.add_txt_field('uwagi',4)
        
    def set_czest(self,m,c):
        self.czest_txt.setText(str(int(m)))
        if c <= 0.5:
            self.rozpr_txt.setText(u'Niski (Dobrze) '+str(c))
        elif 0.5 < c < 0.75:
            self.rozpr_txt.setText(u'Średni '+str(c))
        else:
            self.rozpr_txt.setText(u'Wysoki (Źle) '+str(c))
        
    def validate_info(self):
        typ = ['?','L','P','W']
        dt = get_val_text(self.data_txt)
        if len(dt) < 10:
            return (False,'data')
        autor = get_val_text(self.autor_txt)
        if autor == '':
            return (False,'autor')
        ci = get_index_combo(self.rodzaj_cmb)
        if ci == 0:
            return (False,'ci')
        czest = get_val_text(self.czest_txt)
        if czest == '':
            return (False,'czest')
        uwagi = get_val_text(self.uwagi_txt)
        return (True, {'rodzaj':typ[ci],'data':dt,'autor':autor,'czest':czest,'uwagi':uwagi})
        
    def get_input(self):
        vi = self.validate_info()
        msgs = {'data':u'Nieprawidłowa data', 'autor':u'Nie podano autora','ci':u'Nie wybrano typu badań',
                'czest':u'Nie podano częstotliwości odczytów'}
        if vi[0]:
            return vi[1]
        else:
            QMessageBox.information(self, u'Błąd', msgs[vi[1]])
            return None
            
class DialogDodajTraseGps(QDialog):
    
    ok = False
    def __init__(self,track_list,parent=None):
        QDialog.__init__(self,parent)
        self.setModal(False)
        self.tracks = track_list
        if self.tracks.count() > 0:
            self._track_frags = True
        else:
            self._track_frags = False
        self.init_dialog()
        
    def zapisz(self):
        if self.view.cov >= 0.5:
            answ = QMessageBox.warning(self, u'Ostrzeżenie',u'Wysoki współczynnik zmienności sugeruje, że'
                                       + u'odstępy między odczytami punktów trasy znacząco się różnią.\n'
                                       +u'To może oznaczać, że segmenty trasy zostały zarejetrowane o innych porach\n'
                                       +u'Kliknij TAK aby zatwierdzić wybór i mimo to zapisać trasę w bazie danych'
                                       +u'Kliknij NIE aby wybrać inne fragmenty', buttons = QMessageBox.Ok | QMessageBox.No)
            if answ == QMessageBox.No:
                return
        self.track_info = self.info_form.get_input()
        if self._track_frags:
            self.rs = self.view.get_selected()
            if not self.rs:
                QMessageBox.information(self, u'Błąd', u'Należy wybrać conajmniej jeden fragment trasy') 
        if self.track_info:
            self.ok = True
            self.zakoncz()
        
    def zakoncz(self):
        self.done(0)
    
    def get_track(self):
        if self.ok:
            tr = self.tracks.concat(self.rs)
            return (tr,self.track_info)
        else:
            return None
        
    def init_dialog(self):
        self.setMinimumSize(QSize(800, 0))
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(QLabel(u'Wybierz fragmenty do scalenia w trasę'))
        if self._track_frags:
            self.view = TableGpsTracks(self.tracks.get_segments(),parent=self) #QListWidget(self)
            self.vbox.addWidget(self.view)
        info ={'czest':str(int(self.view.mean))}
        if self.view.cov <= 0.5:
            info['rozpr'] = u'Niski (Dobrze) '+str(self.view.cov)
        elif 0.5 < self.view.cov < 0.75:
            info['rozpr'] = u'Średni '+str(self.view.cov)
        else:
            info['rozpr'] = u'Wysoki (Źle) '+str(self.view.cov)
        self.info_form = FormTracks(parent=self,info=info)
        self.view.set_meanhandler(self.info_form.set_czest)
        self.vbox.addWidget(self.info_form)
        self.button_box = QDialogButtonBox(self)
        self.vbox.addWidget(self.button_box)
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.zapisz)
        self.button_box.rejected.connect(self.zakoncz)

class WyszukajAkcja(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,'Wyszukaj',window)
        self.triggered.connect(self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        trasy = get_warstwa('trasy')
        if trasy is None:
            QMessageBox.warning(self._win,u'Wyszukiwanie',u'Przed wyszukiwaniem należy otworzyć warstwę "trasy"')
            return 
        warunek = QInputDialog.getText(self._win, 'Trasy', 'Wprowadz warunek', text='id > 0')
        if warunek[1]:
            mf = TrasyFrame(szukaj_trasy(str(warunek[0])),self._iface,self._win)
            self._win.dodaj(mf)

class ImportGpsAkcja(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,'Importuj z GPS',window)
        self.triggered.connect(self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        trasy = get_warstwa('trasy')
        if trasy is None:
            QMessageBox.warning(self._win,u'Import GPS',u'Przed importem należy otworzyć warstwę "trasy"')
            return 
        if self._iface:
            fn = QFileDialog.getOpenFileName(self._win, filter='Pliki GPX (*.gpx)')
        else:
            fn = '/home/milosz/archeocs/gpx/miejsca_test.gpx'
        trpts = TrackPoints()
        trpts.create(fn)
        if trpts.count() == 0:
            QMessageBox.warning(self._win,u'Import GPS',u'W pliku GPX nie ma zdefinowanych tras')
            return
        add_dial = DialogDodajTraseGps(trpts,parent=self._win)
        add_dial.exec_()
        nt = add_dial.get_track()
        if nt is None:
            return
        nf, ni = nt[0], nt[1]
        trasy.startEditing()
        #TRASY_ATR = ['id','rozpoczecie','zakonczenie','czestotliwosc','rodzaj_badan','data','autor','uwagi']
        atrs = {1:ni['rodzaj'],2:ni['data'],3:ni['autor'],4:nf.min_czas(),5:nf.max_czas(),
               6:ni['czest'],7:ni['uwagi']}
        dodaj(trasy, atrs, nf.geom())
        if trasy.commitChanges():
            QMessageBox.information(self._win, "Import GPS", u'Nowa trasa została zapisana')
