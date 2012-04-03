# -*- coding: utf-8 -*-

# AZP2-GPS - import danych GPS
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


from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QWidget, QComboBox, QLineEdit
from PyQt4.QtGui import QFormLayout, QMessageBox, QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt4.QtCore import Qt, QSize, SIGNAL
from libazp.gpx import distr, GpxPointsList

def get_val_text(txt_fld):
    return unicode(txt_fld.text())

def get_val_combo(combo):
    return unicode(combo.currentText())

def get_index_combo(combo):
    return combo.currentIndex()

class TableGpsTracks(QTableWidget):
    
    def __init__(self,segments,parent=None):
        QTableWidget.__init__(self,parent)
        self.tracks = []
        self.segments = segments
        self.cov = 0.0
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
                wit = QTableWidgetItem(unicode(f))
            wit.setToolTip(unicode(f))
            #wit.sets
            self.setItem(rindex,fi,wit)     
    
    #def get_row(self,row):
    #    return [self.item(row, 0).data(Qt.CheckStateRole).toInt(),unicode(self.item(row,5).text()),unicode(self.item(row,6).text())]
    
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
        self.con_list = GpxPointsList()
        for s in self.segments:
            self.add_row([True,s.min_time(),s.max_time(),s.first().wkt(),s.last().wkt(),s.count()]) 
            self.con_list += s
        d = distr(self.con_list.time_deltas())
        self.cov = round(d[1] / d[0],2)# / d[0]
        self.mean = round(d[0],2)
        self.resizeColumnsToContents()
        self.connect(self, SIGNAL('itemClicked(QTableWidgetItem *)'),self._update_cov)
    
    def set_meanhandler(self,h):
        self._handler_mean = h
        
    def _update_cov(self,it):
        if it.column() == 0:
            self.con_list = GpxPointsList()
            for s in self.get_selected():
                self.con_list += self.segments[s]
            d = distr(self.con_list.time_deltas())
            self.cov = round(d[1] / d[0],2)
            self.mean = round(d[0],2)
            if self._handler_mean:
                self._handler_mean(self.mean,self.cov)
        else:
            self._handler_mean(it.column())
        
class FormInfoTracks(QWidget):
    
    _form_fields = [u'Data pomiarów', u'Autor', u'Rodzaj badań', u'Częstotliwość odczytu', u'Uwagi',u'Współczynnik zmienności']
    def __init__(self,parent=None,info={}):
        QWidget.__init__(self,parent)
        self.info = info
        self.init_form()
    
    def add_txt_field(self,key,label_id):
        fld = QLineEdit() 
        if self.info.has_key(key):
            fld.setText(self.info[key])
        self.form.addRow(self._form_fields[label_id], fld)
        return fld
    
    def add_combo_field(self,label_id,values=[u'Wybierz'],ch=0):
        combo = QComboBox()
        combo.addItems(values)
        if ch < len(values):
            combo.setCurrentIndex(ch)
        else:
            combo.setCurrentIndex(0)
        self.form.addRow(self._form_fields[label_id], combo)
        return combo
        
    def init_form(self):
        self.form = QFormLayout(self)
        self.data_txt = self.add_txt_field('data', 0)
        self.data_txt.setInputMask('0000-00-00')
        self.autor_txt = self.add_txt_field('autor', 1)
        self.rodzaj_cmb = self.add_combo_field(2,[u'Nieokreślony',u'Lot',u'Powierzchniowe',u'Weryfikacja'], 0)
        self.czest_txt = self.add_txt_field('czest', 3)
        self.rozpr_txt = self.add_txt_field('rozpr', 5)
        self.rozpr_txt.setReadOnly(True)
        self.czest_txt.setInputMask('000')
        self.uwagi_txt = self.add_txt_field('uwagi', 4)
        
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

class DialogAddGpsTracks(QDialog):
    
    ok = False
    def __init__(self,track_list,parent=None):
        QDialog.__init__(self,parent)
        self.setModal(False)
        self.tracks = track_list
        if self.tracks.count() > 1:
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
            print self.rs
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
        if self._track_frags:
            self.vbox.addWidget(QLabel(u'Wybierz fragmenty do scalenia w trasę'))
            self.view = TableGpsTracks(self.tracks.get_segments(),parent=self) #QListWidget(self)
            self.vbox.addWidget(self.view)
        info ={'czest':str(int(self.view.mean))}
        if self.view.cov <= 0.5:
            info['rozpr'] = u'Niski (Dobrze) '+str(self.view.cov)
        elif 0.5 < self.view.cov < 0.75:
            info['rozpr'] = u'Średni '+str(self.view.cov)
        else:
            info['rozpr'] = u'Wysoki (Źle) '+str(self.view.cov)
        self.info_form = FormInfoTracks(parent=self,info=info)
        self.view.set_meanhandler(self.info_form.set_czest)
        self.vbox.addWidget(self.info_form)
        self.button_box = QDialogButtonBox(self)
        self.vbox.addWidget(self.button_box)
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.connect(self.button_box,SIGNAL('accepted()'),self.zapisz)
        self.connect(self.button_box,SIGNAL('rejected()'),self.zakoncz)