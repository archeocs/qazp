# -*- coding: utf-8 -*-

'''
Created on Mar 23, 2012

@author: milosz
'''
from PyQt4.QtCore import QObject, SIGNAL,QSize,Qt
from PyQt4.QtGui import QAction, QMessageBox, QDialog,QVBoxLayout,QDialogButtonBox,QApplication
from PyQt4.QtGui import QTableWidget,QTableWidgetItem,QFileDialog
from libazp.qgs import Layer
#import logging
from libazp.gpx import TrackList

class Plugin(object):
    
    def __init__(self,iface):
        self.iface = iface
        #logging.basicConfig(filename='',level=logging.INFO)
    
    def initGui(self):
        self.akcja = QAction("Importuj plik GPX", self.iface.mainWindow())
        self.akcja.setWhatsThis("Dane GPS")
        self.akcja.setStatusTip("GPS")
        QObject.connect(self.akcja, SIGNAL("triggered()"), self.run)

        self.iface.addToolBarIcon(self.akcja)
        self.iface.addPluginToMenu("AZP2-GPS",self.akcja)
    
    def unload(self):
        self.iface.removePluginMenu("GpsAzp",self.akcja)
        self.iface.removeToolBarIcon(self.akcja)
    
    def run(self):
        lay = Layer('podroze')
        if lay.layer: # udalo sie wyszukac
            file_gpx = QFileDialog.getOpenFileName(self.iface.mainWindow(), filter='Pliki GPX (*.gpx)')
            td = TracksDialog(file_gpx,layer=lay,parent=self.iface.mainWindow())
            td.exec_()
            if td.features:
                QMessageBox.information(self.iface.mainWindow(), 'Info',u"Dodano "+str(len(td.features))+u" obiektów " )
                lay.layer.setSelectedFeatures([f.id()*-1 for f in td.features])
                self.iface.mapCanvas().zoomToSelected()
        else:
            QMessageBox.information(self.iface.mainWindow(), 'Info',u"Nie udało się znaleźć warstwy 'podroze'."+
                                                                u" Sprawdź, czy zostało nawiązane połączenie z bazą danych" )   
        
class TracksTable(QTableWidget):
    
    def __init__(self,tracks=[],parent=None):
        QTableWidget.__init__(self,parent)
        self.tracks = []
        for t in tracks:
            self.tracks.append(list(t)) 
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
    
    def get_row(self,row):
        return [self.item(row, 0).data(Qt.CheckStateRole).toInt(),unicode(self.item(row,5).text()),unicode(self.item(row,6).text())]
        
    def init_tab(self):
        self.setWordWrap(True)
        self.setColumnCount(8)
        self.setHorizontalHeaderLabels([u'Dodaj', u'Data rozpoczęcia', u'Data zakończenia',u'Pierwszy punkt',
                                        u'Ostatni punkt',u'Autor',u'Opis',u'Liczba punktów'])   
        self.resizeColumnsToContents()
        for t in self.tracks:
            self.add_row([True,t[1],t[2],t[0].first(),t[0].last(),u'',u'',t[3]]) 
        
        
class TracksDialog(QDialog):
    
    def __init__(self,gpx,layer=None,parent=None):
        QDialog.__init__(self,parent)
        self.setWindowTitle('AZP2-GPS')
        self.layer = layer
        self.tracks = self.tracks_list(gpx)
        self.features = []
        self.init_dialog()
        
    def init_dialog(self,tracks=[]):
        self.setMinimumSize(QSize(800, 0))
        self.vbox = QVBoxLayout(self)
        self.view = TracksTable(self.tracks,parent=self) #QListWidget(self)
        self.vbox.addWidget(self.view)
        self.button_box = QDialogButtonBox(self)
        self.vbox.addWidget(self.button_box)
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.connect(self.button_box,SIGNAL('accepted()'),self.zapisz)
        self.connect(self.button_box,SIGNAL('rejected()'),self.zakoncz)
        
    def tracks_list(self,gpx_file):
        return TrackList().get_list(gpx_file)
    
    def zapisz(self):
        if self.layer:
            self.layer.edit()
            for i in range(self.view.rowCount()):
                row = self.view.get_row(i)
                if row[0][0] == Qt.Checked:
                    line = self.tracks[i][0]
                    nid = self.layer.max_id()+1
                    desc = row[2]
                    auth = row[1]
                    stime = self.tracks[i][1]
                    etime = self.tracks[i][2]
                    af = self.layer.add_feature(line,atr=[nid,desc,auth,stime,etime])
                    if af[0]:
                        self.features.append(af[1])
            self.layer.save()
        self.zakoncz()
    
    def zakoncz(self):
        self.done(0)

def main():
    from sys import argv
    app = QApplication(argv)
    td = TracksDialog('/home/milosz/archeocs/gpx/test.gpx')
    td.exec_()
    
if __name__ == '__main__':
    main()