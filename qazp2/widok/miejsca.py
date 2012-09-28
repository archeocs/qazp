'''
Created on Sep 9, 2012

@author: milosz
'''

from geom import GTabModel, GFrame
from PyQt4.QtGui import QMessageBox, QAction, QDialog, QFormLayout, QVBoxLayout, QWidget, QDialogButtonBox, QLineEdit  
from PyQt4.QtGui import QInputDialog, QFileDialog,QComboBox,QPlainTextEdit
from PyQt4.QtCore import QObject,SIGNAL,QVariant
from PyQt4.uic import loadUi
from lib.miejfun import wybrane,pobierz,zamien,dodaj,usun,zmien2
from lib.gps import WayPoints
from dane.zrodla import rejestr_map, get_warstwa
from qgis.core import QgsDataSourceURI
from functools import partial
from os.path import abspath


def tab_model(obiekty,parent=None):
    return GTabModel(['Ident','Nazwa','Rodzaj','Data','Autor','Uwagi'],obiekty,parent)

def txt(v,trim=False,mx=-1):
    if not v:
        return ""
    if isinstance(v, QVariant):
        u = unicode(v.toString())
    else:
        u = unicode(v)
    if trim:
        u = u.strip()
    if mx > 0:
        u = u[:mx]
    return u

class MiejscaDialog(QDialog):
    
    def __init__(self,dane=None,parent=None):
        QDialog.__init__(self,parent)
        self.dane = dane
        self.init_dialog(dane)
        
    def init_dialog(self,dane):
        vbox = QVBoxLayout(self)
        self.setLayout(vbox)
        wgt = QWidget(self)
        form = QFormLayout(wgt)
        self.nazwa_txt, self.rodz_txt, self.dt_txt = QLineEdit(parent=self),QLineEdit(parent=self),QLineEdit(parent=self)
        self.autor_txt, self.uwagi_txt = QLineEdit(parent=self),QLineEdit(parent=self)
        wgt.setLayout(form)
        form.addRow('Nazwa', self.nazwa_txt)
        form.addRow('Rodzaj', self.rodz_txt)
        form.addRow('Data', self.dt_txt)
        form.addRow('Autor', self.autor_txt)
        form.addRow('Uwagi', self.uwagi_txt)
        vbox.addWidget(wgt)
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.connect(bb,SIGNAL('accepted()'), self.accept);
        self.connect(bb,SIGNAL('rejected()'), self.reject);
        vbox.addWidget(bb)
        self.setWindowTitle('id: '+txt(dane['id'])+" "+str(dane.feature().id()))
        if dane is not None:
            self.nazwa_txt.setText(txt(dane['nazwa'],True))
            self.rodz_txt.setText(txt(dane['rodzaj_badan'],True))
            self.dt_txt.setText(txt(dane['data'],mx=10))
            self.autor_txt.setText(txt(dane['autor'],True))
            self.uwagi_txt.setText(txt(dane['uwagi'],True))
        self.setModal(True)
    
    def get_dane(self):
        return {'nazwa':self.nazwa_txt.text(),'rodzaj_badan':self.rodz_txt.text(),'data':self.dt_txt.text(),
                'autor':self.autor_txt.text(),'uwagi':self.uwagi_txt.text()}
        
def eddial(dane):
    dial = loadUi(abspath(__file__+'/../../forms/miejsca.ui'))
    txt_naz = dial.findChild(QLineEdit,'nazwa')
    txt_naz.setText(txt(dane['nazwa']))
    
    cb_rodz = dial.findChild(QComboBox,'rodzaj_badan')
    rb = dane['rodzaj_badan']
    mpi = {'?':0,'P':1,'L':2}
    if rb is None:
        cb_rodz.setCurrentIndex(0)
    else:
        cb_rodz.setCurrentIndex(mpi[str(rb.toString())])
    
    txt_dt = dial.findChild(QLineEdit,'data')
    txt_dt.setText('2012-01-01')
    txt_autor = dial.findChild(QLineEdit,'autor')
    txt_autor.setText(txt(dane['autor']))
    txt_uwagi = dial.findChild(QPlainTextEdit,'uwagi')
    txt_uwagi.setPlainText(txt(dane['uwagi']))
    zatw_part = partial(zatwierdzone,dial=dial,fid=dane.feature().id(),feature=dane.feature())
    bb = dial.findChild(QDialogButtonBox,'buttonBox')
    QObject.connect(bb, SIGNAL('accepted()'),zatw_part)
    dial.setModal(True)
    return dial
    
def zatwierdzone(dial,fid,feature,ed=False):
    if dial is None:
        return
    txt_naz = dial.findChild(QLineEdit,'nazwa') 
    cb_rodz = dial.findChild(QComboBox,'rodzaj_badan')
    txt_dt = dial.findChild(QLineEdit,'data')
    txt_autor = dial.findChild(QLineEdit,'autor')
    txt_uwagi = dial.findChild(QPlainTextEdit,'uwagi')
    ma = feature.attributeMap()
    nv = {0:ma[0],1:txt_naz.text(),3:txt_dt.text(),
                4:txt_autor.text(),5:txt_uwagi.toPlainText()}
    mpi = {0:'?',1:'P',2:'L'}
    nv[2] = QVariant(mpi[cb_rodz.currentIndex()]).toString()
    feature.setAttributeMap(nv)
    

class MiejscaFrame(GFrame):
    
    warstwa = None
    def __init__(self,warstwa,iface,parent=None):
        GFrame.__init__(self,pobierz(warstwa),parent)
        self.warstwa = warstwa
        self._if = iface
        self._win = parent
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
        #dialog = MiejscaDialog(dane=self.wybrany_wiersz()[1])
        ww = self.wybrany_wiersz()[1]
        dialog = eddial(ww)
        r = dialog.exec_()
        if r != QDialog.Rejected:
            z = zmien2(self.warstwa,ww.feature())
            if z:
                ww.aktualizuj()
                QMessageBox.information(self, 'info', 'Zmienione')
        #if r == QDialog.Accepted:
        #    ww = self.wybrany_wiersz()[1]
        #    ww.zmien(dialog.get_dane())
        #    ww.zatwierdz()
        #    z = zamien(self.warstwa,ww)
        #    if z[0]:
        #        QMessageBox.information(self, 'info', 'Zmienione')
                
    def akcja_usun(self):
        ww = self.wybrany_wiersz()[1]
        u = usun(self.warstwa,ww)
        if u:
            QMessageBox.information(self, 'info', u'Usuniete miejsce %s'%unicode(ww['nazwa'].toString()))
            
def formularz(dialog,fid,feature):
    txtNaz = dialog.findChild(QLineEdit,"nazwa")
    txtNaz.setText(u'Nowa')

class WyszukajAkcja(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,'Wyszukaj',window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        warunek = QInputDialog.getText(self._win, 'Miejsca', 'Wprowadz warunek', text='id > 0')
        if warunek[1]:
            mf = MiejscaFrame(wybrane(unicode(warunek[0])),self._iface,self._win)
            self._win.setCentralWidget(mf)

class ImportGpsAkcja(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,'Importuj z GPS',window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface
        
    def wykonaj(self):
        if self._iface:
            fn = QFileDialog.getOpenFileName(self._win, filter='Pliki GPX (*.gpx)')
        else:
            fn = '/home/milosz/archeocs/gpx/miejsca_test.gpx'
        wp = WayPoints()
        wp.create(fn)
        if self._iface is None:
            QMessageBox.information(self._win, 'Import GPS', 'Odczytano %d punktow'%len(wp.pts_list))
        miejsca = get_warstwa("miejsca")
        miejsca.startEditing()
        for (pi,p) in enumerate(wp.pts_list):
            m = p.mapa()
            m[1] = 'punkt %d'%pi
            dodaj(miejsca, m, p.geom())
        if miejsca.commitChanges():
            QMessageBox.information(self._win, 'Import GPS', 'Zapisano %d punktow'%len(wp.pts_list))

class TestUri(QAction):
    
    def __init__(self,iface,window):
        QAction.__init__(self,'Test uri',window)
        QObject.connect(self, SIGNAL('triggered()'), self.wykonaj)
        self._win = window
        self._iface = iface  
        
    def wykonaj(self):
        mw = get_warstwa("miejsca")
        QMessageBox.information(self._win, 'test', QgsDataSourceURI(mw.dataProvider().dataSourceUri()).sql())
        
    
        
    