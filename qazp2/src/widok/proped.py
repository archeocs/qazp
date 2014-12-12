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

from PyQt4.QtGui import QStyledItemDelegate, QComboBox, QTableView, QAbstractItemView 
from PyQt4.QtGui import   QHeaderView,QFrame,QDialogButtonBox,QVBoxLayout
from PyQt4.QtCore import QVariant, QAbstractTableModel, Qt
from functools import partial
from dane.zrodla import getPolaczenie2
from lib.qgsop import setMapa, zmien
import logging

def conw(w,slow):
    if isinstance(w, QVariant):
        klucz = str(w.toString()).upper()
    else:
        klucz = str(w).upper()
    if slow.has_key(klucz):
        return slow[klucz]
    return None

class WyborDelegate(QStyledItemDelegate):

    def __init__(self,parent=None):
        QStyledItemDelegate.__init__(self,parent)
        self._opt = {}
        self._con = {}
    
    def setOpcja(self,r,op):
        self._opt[r] = op
        
    def setDb(self,r,con):
        self._con[r] = con
        
    def getDane(self,pc):
        con = getPolaczenie2(pc[0])
        stmt = 'select id,nazwa from '+pc[1]+' order by nazwa'
        ret = con.wszystkie(stmt)
        con.zakoncz()
        return ret  

    def createEditor(self,parent,styl,indeks):
        self.initStyleOption(styl,indeks)
        c = indeks.column()
        if c == 1:
            if self._opt.has_key(indeks.row()):
                tw = self._opt[indeks.row()]
            elif self._con.has_key(indeks.row()):
                tw = self.getDane(self._con[indeks.row()])
            else:
                return QStyledItemDelegate.createEditor(self,parent,styl,indeks)
            cb = QComboBox(parent)
            for o in tw:
                cb.addItem(o[1],o[0])
            cb.addItem(u'Nieokreślone',QVariant())
            return cb
        return None
 
    def setEditorData(self,edytor,indeks):
        di = indeks.data()
        if self._opt.has_key(indeks.row()) or self._con.has_key(indeks.row()):
            for i in range(edytor.count()):
                if edytor.itemText(i) == di:
                    edytor.setCurrentIndex(i)
                    return
            edytor.setCurrentIndex(edytor.count()-1) # wartosc nieokreslona
        else:
            QStyledItemDelegate.setEditorData(self,edytor,indeks)
    
    def setModelData(self,edytor,model,indeks):
        if self._opt.has_key(indeks.row()) or self._con.has_key(indeks.row()):
            d = edytor.itemData(edytor.currentIndex())
            model.setData(indeks,d)
        else:
            model.setData(indeks,QVariant(edytor.text()))

class PropLista(QAbstractTableModel):
    
    def __init__(self,opt,dane,parent=None): # dane = slownik {klucz:wartosc}
        QAbstractTableModel.__init__(self,parent)
        self._opt = opt
        self._dane = dane
        self._wid = {}
        
    def rowCount(self, *args, **kwargs):
        return len(self._opt)
    
    def columnCount(self, *args, **kwargs):
        return 2
    
    def data(self, indeks, rola = Qt.DisplayRole):
        r,c = indeks.row(), indeks.column()
        if rola == Qt.DisplayRole:
            if c == 0:
                return self._opt[r][0]
            elif c == 1 and self._dane.has_key(self._opt[r][1]):
                if not self._wid.has_key(self._opt[r][1]):
                    self._wid[self._opt[r][1]] = self._opt[r][2](self._dane[self._opt[r][1]]) 
                return self._wid[self._opt[r][1]]
        elif rola == Qt.EditRole and c == 1 and self._dane.has_key(self._opt[r][1]):
            if not self._wid.has_key(self._opt[r][1]):
                self._wid[self._opt[r][1]] = self._opt[r][2](self._dane[self._opt[r][1]]) 
            return self._wid[self._opt[r][1]]
        return QVariant()
    
    def setData(self,indeks, wartosc, rola=Qt.EditRole):
        r,c = indeks.row(), indeks.column()
        if rola == Qt.EditRole and c == 1:
            self._dane[self._opt[r][1]] = wartosc
            self._wid.pop(self._opt[r][1],'')
            #logging.info("Wstawiona wartosc: "+unicode(wartosc.toString())+"$")
            return True
        return False
            #self.dataChanged(indeks,indeks)
    
    def flags(self,indeks):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable
    
    def headerData(self, sekcja, orientacja, rola = Qt.DisplayRole):
        if orientacja == Qt.Vertical:
            return None
        if sekcja < 0 or sekcja >= 2:
            raise Exception("headerData: indeks %d poza zakresem [0,%d]"%(sekcja,len(self._nag)-1))
        if rola == Qt.DisplayRole:
            if sekcja == 0:
                return u'Nazwa'
            elif sekcja == 1:
                return u'Wartość'

class PropWidok(QTableView):
    
    vb = [('T','Tak'),('N','Nie')]
    vr = [('M',u'Mała'),( 'S',u'Średnia'),( 'D',u'Duża')]
    ve = [('I',u'Istnieje'),( 'N',u'Nie istnieje')]
    
    wb = partial(conw,slow=dict(vb))
    wr = partial(conw,slow=dict(vr))
    we = partial(conw,slow=dict(ve))
    
    def __init__(self,dane=None,parent=None):
        QTableView.__init__(self,parent)
        self._del = WyborDelegate(parent=self)
        self.setItemDelegate(self._del)
        self.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.AnyKeyPressed)
    
    def dodajOpt(self,r,v):
        self._del.setOpcja(r,v)
        return self
        
    def dodajDb(self,r,d):
        self._del.setDb(r,d)
        return self
    
    def dodTn(self,r):
        self._del.setOpcja(r,self.vb)
    
    def setDelegat(self,opcje,w):
        self.setItemDelegate(WyborDelegate(opcje,parent=self))
        print 'ok'
        
    def ustawModel(self,dane,opcje):
        self.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        if not dane:
            self._dane = {}
        else:
            self._dane = dane
        _mod = PropLista(opcje,self._dane,parent=self)
        self.setModel(_mod)
        self.horizontalHeader().setResizeMode(QHeaderView.Stretch)
    
    def konwert(self, dane):
        rd = {}
        for (k,v) in dane.iteritems():
            if isinstance(v, QVariant):
                if v.isNull():
                    rd[k] = None
                    continue
                t = v.type()
                if t == QVariant.Int:
                    rd[k] = v.toInt()[0]
                elif t == QVariant.Double:
                    rd[k] = v.toDouble()[0]
                elif t == QVariant.DateTime:
                    rd[k] = v.toDateTime().toString(Qt.ISODate)
                elif t == QVariant.DateTime:
                    rd[k] = v.toDate().toString(Qt.ISODate)
                else:
                    rd[k] = unicode(v.toString())
            else:
                rd[k] = unicode(v)
        return rd
        
    def wartosci(self):
        return self.konwert(self._dane)
    
    def aktualizujId(self, nowyId=None):
        if nowyId is not None:
            self._dane['id'] = nowyId
        
    def nic(self,w):
        return w
    
class PropFrame(QFrame):
    def __init__(self, warstwa, dane, win, atrybuty, widokCls, parent=None):
        QFrame.__init__(self,parent)
        self._dane = dane
        self._win = win
        self._war = warstwa
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self._widok = widokCls(self._dane,self)
        vbox.addWidget(self._widok)
        bb = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close)
        bb.accepted.connect(partial(self._zapisz, atr=atrybuty))
        bb.rejected.connect(self._zamknij)
        vbox.addWidget(bb)
        
    def _zapisz(self, atr):
        obj = self._dane.feature()
        wart = self._widok.wartosci()
        setMapa(obj, wart, atr)
        #logging.info("Zapisuje wartosci "+wart)
        if zmien(self._war,obj):
            self._win.statusBar().showMessage('Zapisano zmiany')
        else:
            self._win.statusBar().showMessage('Blad zapisu')
    
    def _zamknij(self):
        self._win.usun(self)
