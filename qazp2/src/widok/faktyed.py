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

from PyQt4.QtGui import QWidget, QLabel, QComboBox, QDoubleSpinBox, QGridLayout, QPushButton, QLineEdit
from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant
from dane.zrodla import FaktyWykaz

class FaktyWykModel(QAbstractTableModel):
    
    KodRola = 100
    
    def __init__(self,jedwyk, parent=None):
        QAbstractTableModel.__init__(self)
        self._jw = jedwyk
        
    def rowCount(self, *args, **kwargs):
        return len(self._jw)
    
    def columnCount(self, *args, **kwargs):
        return 1
        
    def data(self, indeks, rola = Qt.DisplayRole):
        if rola == Qt.DisplayRole:
            return QVariant(self._jw[indeks.row()])
        else:
            return QVariant(self._jw.kod(indeks.row()))
        
class Fakty(object):
    
    fkatr = ['id', 'f.okres','jed1', 'jed2', 'relacja','pewnosc','u.funkcja', 'rodzaj_fun', 
                'masowy', 'wydzielony', 'ja.nazwa', 'ja.skrot', 'jb.nazwa', 'jb.skrot', 'u.nazwa', 'u.skrot']
    def __init__(self,st,con):
        self.selFk = con.prep('select '+(','.join(self.fkatr))+' from fakty f left outer join jednostki ja on f.jed1 = ja.kod '+
                                'left outer join jednostki jb on f.jed2 = jb.kod left outer join funkcje u on f.rodzaj_fun = u.kod '+
                                'where stanowisko ='+str(st))
        self.insFk = con.prep("insert into fakty values(:id,"+str(st)+" ,:okres,:jed1,:jed2,:relacja,:pewnosc,:funkcja,"+
                                                        ":rodzaj_fun,:masowy,:wydzielony)")
        self.updtFk = con.prep('update fakty set okres=:okres, funkcja=:funkcja, jed1=:jed1, jed2=:jed2, relacja=:relacja,'+
                               ' pewnosc=:pewnosc, masowy=:masowy, wydzielony=:wydzielony, rodzaj_fun=:rodzaj_fun where id=:id'+
                               ' and stanowisko='+str(st))
        self.delFk = con.prep('delete from fakty where id=:id and stanowisko='+str(st))
        self._p = con
        self._odswiez()
        
    def _odswiez(self):    
        self._fk = []
        for f in self.selFk.wszystkie():
            self._fk.append(dict([(ei,e) for (ei, e) in enumerate(f)]))
   
    def __len__(self):
        return len(self._fk)
    
    def __getitem__(self, i):
        if i < len(self._fk):
            f = self._fk[i]
            return {'okres':f[1], 'jed1':f[2], 'jed2':f[3], 'relacja':f[4], 'pewnosc':float(f[5]), 'funkcja':f[6], 'rodzaj_fun':f[7], 'masowy':f[8], 'wydzielony':f[9], 'id':f[0]}
        return {}
    
    def _krep(self,r):
        f = self._fk[r]
        kw = f[11]
        if f[3] is not None:
            if f[4] == 'O':
                kw += '-'+f[13]
            elif f[4] == 'L':
                kw += '/'+f[13]
        if float(f[5]) < 1:
            kw = '?'+kw
        return kw
    
    def _frep(self,r):
        f = self._fk[r]
        if f[7] is not None:
            return f[15]
        elif f[6] is not None:
            return f[6]
        return None        
    
    def wget(self, r, c):
        if r >= len(self._fk):
            return QVariant()
        elif c == 0:
            return QVariant(r+1)
        elif c == 1:
            return QVariant(self._fk[r][1])
        elif c == 2:
            return QVariant(self._krep(r)) # reprezentacja kultury
        elif c == 3:
            return QVariant(self._frep(r))
        elif c == 4:
            return QVariant(self._fk[r][8])
        elif c == 5:
            return QVariant(self._fk[r][9])
        return QVariant()
     
    def wset(self, r, c, v):
        if r == len(self._fk):
            self._fk.append[{}]
        self._fk[r][c] = v
    
    def _poprDane(self,dane):
        if dane['relacja'] is None or dane['relacja'].strip() == '':
            dane['relacja'] = 'null'
            dane['jed2'] = 'null'
        for (k,v) in dane.iteritems():
            if v is None:
                dane[k] = 'null'
            elif isinstance(v,(str,unicode)) and v != 'null':
                dane[k] = "'%s'" % v
        return dane
    
    _cmpTab = ['id','okres','jed1','jed2','relacja','pewnosc','funkcja','rodzaj_fun','masowy','wydzielony']    
    def cmpMapy(self, d, f):
        for (ci, c) in enumerate(self._cmpTab):
            if ci > 0 and d.get(c) != f.get(ci):
                #print d[c], f[ci]
                return False # dane roznia sie miedzy soba
        return True
    
    def zmien(self, r, dane):
        if self.cmpMapy(dane,self._fk[r]):
            return (False,'')
        if dane['id'] == -1:
            return (False,'Taki fakt nie istnieje w bazie')
        self.updtFk.wykonaj(dane,False)
        self._odswiez()
        return (True,'')
        
    def usun(self,dane):
        self.delFk.wykonaj(dane,False)
        self._odswiez()
        return (True,'')
    
    def dodaj(self, dane):
        ni = self._p.jeden('select coalesce(max(id),0) from fakty')[0]+1
        dane['id'] = ni
        print self.insFk._ps
        self.insFk.wykonaj(dane,False)
        self._odswiez()
        
class FModel(QAbstractTableModel):

    def __init__(self,fakty,parent=None):
        QAbstractTableModel.__init__(self,parent)
        self._fk = fakty
        self._nag = [u'Nr', u'Okres', u'Kultura', u'Funkcja', u'Masowy', u'Wydzielony']

    def rowCount(self, *args, **kwargs):
        return len(self._fk)+1
    
    def columnCount(self, *args, **kwargs):
        return 6
    
    def data(self, indeks, rola = Qt.DisplayRole):
        if rola == Qt.DisplayRole:
            r,c = indeks.row(), indeks.column()
            return self._fk.wget(r,c)
        
    def headerData(self, sekcja, orientacja, rola = Qt.DisplayRole):
        if orientacja == Qt.Vertical:
            return None
        if sekcja > len(self._nag):
            raise Exception("headerData: indeks %d poza zakresem [0,%d]"%(sekcja,len(self._nag)-1))
        elif rola == Qt.DisplayRole:
            return QVariant(self._nag[sekcja])
        return QVariant() 

def wypCb(cb, tab):
    for t in tab:
        cb.addItem(t[0],t[1])
        
class EdWgt(QWidget):
    
    def _dodajEt(self,lay,et):
        for (ei,e) in enumerate(et):
            lay.addWidget(QLabel(e),0,ei)
    
    def _dodajWgt(self,lay,wgt):
        for (wi,w) in enumerate(wgt):
            lay.addWidget(w,1,wi)        
    
    def __init__(self,con,parent=None):
        QWidget.__init__(self)
        self._con = con
        hbox = QGridLayout()
        self.setLayout(hbox)
        self._okrCb, self._j1Cb, self._relCb, self._j2Cb, self._funCb = QComboBox(),QComboBox(),QComboBox(),QComboBox(),QComboBox()
        self._masTxt, self._wydzTxt, self._rodzCb, self._pewTxt = QLineEdit(), QLineEdit(), QComboBox(), QDoubleSpinBox()
        self._dodBtn, self._usuBtn = QPushButton('Dodaj'),QPushButton(u'Usuń')
        self._modAct, self._usuAct = None, None
        self._dodajEt(hbox, ['Okres','Jednostka','Relacja','Jednostka',u'Pewność',u'Funkcja',u'Rodzaj','Masowy','Wydzielony'])
        self._dodajWgt(hbox, [self._okrCb,self._j1Cb,self._relCb,self._j2Cb,self._pewTxt,self._funCb,
                              self._rodzCb,self._masTxt,self._wydzTxt,self._dodBtn,self._usuBtn])
        wypCb(self._okrCb,[(u'Nieokreślona',None),('Paleolit','P'),('Mezolit','M'),('Mezolit/Neolit','L'),
                           ('Neolit','N'),(u'E. Brązu','B'),(u'E. Żelaza','Z')])
        self._okrCb.currentIndexChanged.connect(self._okrZm)
        wypCb(self._funCb,[(u'Nieokreślona', None),('GOSPODARCZA','G'),(u'KOMPLEKS OSADNICZY','K'),('KOPIEC','P'),
                           ('OBRONNA','O'),(u'OBRZĘDOWA','B'),('OSADNICZA','M'),('POLE BITWY','T'),('SEPULKRALNA','S'),
                           ('SKARB','R'),('STANOWISKO','A'),('ST. REDEPONOWANE','D'),(u'WAŁY','W'),(u'LUŹNE','L')])
        wypCb(self._relCb,[(u'Brak',None),(u'Lub [/]','L'),(u'Oraz','O')])
        self._funCb.currentIndexChanged.connect(self._funZm)
        self._j2Cb.setEnabled(False)
        self._relCb.currentIndexChanged.connect(self._relZm)
        self._dodBtn.clicked.connect(self._modKlik)
        self._usuBtn.clicked.connect(self._delKlik)
        self._jw = FaktyWykaz('jednostki','okres')
        self._fw = FaktyWykaz('funkcje','funkcja')
        self._jm1, self._jm2 = FaktyWykModel(self._jw), FaktyWykModel(self._jw)
        self._fm = FaktyWykModel(self._fw)
        self._j1Cb.setModel(self._jm1)
        self._j2Cb.setModel(self._jm2)
        self._rodzCb.setModel(self._fm)
        #self._funCb.setModel(self._fm)
    
    okrTab = [None,'P','M','L','N','B','Z']
    funTab = [None,'G','K','P','O','B','M','T','S','R','A','D','W','L']

    relTab = [None,'L','O']
    bid = -1
    
    def setDane(self,dd,nowy=False):
        v = dd.get('okres')
        if v == '':
            v = None
        self._okrCb.setCurrentIndex(self.okrTab.index(v))
        self._j1Cb.setCurrentIndex(self._jw.indeks(dd.get('jed1',None)))
        self._relCb.setCurrentIndex(self.relTab.index(dd.get('relacja',None)))
        self._j2Cb.setCurrentIndex(self._jw.indeks(dd.get('jed2',None)))
        v = dd.get('funkcja')
        if v == '':
            v = None
        self._funCb.setCurrentIndex(self.funTab.index(v))
        self._rodzCb.setCurrentIndex(self._fw.indeks(dd.get('rodzaj_fun',None)))
        #self._funTxt.setText(dd.get('funkcja',""))
        self._masTxt.setText(unicode(dd.get('masowy','')))
        self._wydzTxt.setText(unicode(dd.get('wydzielony','')))
        self._pewTxt.setValue(dd.get('pewnosc',1))
        self.bid = dd.get('id',-1)
        if nowy:
            self._dodBtn.setText('Dodaj')
        else:
            self._dodBtn.setText(u'Zmień')
    
    def setModAct(self,a):
        self._modAct = a
        
    def setUsuAct(self,a):
        self._usuAct = a
    
    def _ci(self,cb):
        return unicode(cb.itemData(cb.currentIndex()).toString())
    
    def getDane(self):
        return {'okres':self._ci(self._okrCb), 'jed1':self._ci(self._j1Cb), 'funkcja':self._ci(self._funCb), 
                'rodzaj_fun':self._ci(self._rodzCb),
            'masowy':unicode(self._masTxt.text()), 'wydzielony':unicode(self._wydzTxt.text()),
            'pewnosc':self._pewTxt.value(), 'relacja':self._ci(self._relCb), 'jed2':self._ci(self._j2Cb),'id':self.bid}
    
    def _relZm(self,i):
        self._j2Cb.setEnabled(i > 0)
        
    def _okrZm(self,i):
        ko = unicode(self._okrCb.itemData(i).toString())
        self._jm1.beginResetModel()
        self._jm2.beginResetModel()
        self._jw.wybor(self._con,ko)
        self._jm2.endResetModel()
        self._jm1.endResetModel()
        
    def _funZm(self,i):
        ko = unicode(self._funCb.itemData(i).toString())
        self._fm.beginResetModel()
        self._fw.wybor(self._con,ko)
        self._fm.endResetModel()
        
    def _modKlik(self):
        if self._modAct is not None:
            self._modAct(self.getDane())
    
    def _delKlik(self):
        if self._usuAct is not None:
            self._usuAct(self.getDane())