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

from functools import partial
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QAction, QMessageBox, QApplication
from PyQt4.QtGui import QFileDialog,QHBoxLayout,QPushButton,QMainWindow,QFrame
from libazp.qgs import Layer
from libazp.gpx import TrackPoints
from gui import DialogAddGpsTracks

class Plugin(object):
    
    def __init__(self,iface):
        self.iface = iface
    
    def initGui(self):
        self.akcja = QAction("Importuj plik GPX", self.iface.mainWindow())
        self.akcja.setWhatsThis("Dane GPS")
        self.akcja.setStatusTip("GPS")
        QObject.connect(self.akcja, SIGNAL("triggered()"), self.run)

        self.iface.addToolBarIcon(self.akcja)
        self.iface.addPluginToMenu("AZP2-GPS",self.akcja)
    
    def unload(self):
        self.iface.removePluginMenu("AZP2-GPS",self.akcja)
        self.iface.removeToolBarIcon(self.akcja)
        
    def run(self):
        main(self.iface.mainWindow(),self.iface)
    

def add_track(self,parent=None,iface=None):
    tracks_layer = Layer('trasy')
    if (tracks_layer.layer and iface) or not iface:
        if iface:
            fn = QFileDialog.getOpenFileName(iface.mainWindow(), filter='Pliki GPX (*.gpx)')
        else:
            fn = '/home/milosz/archeocs/gpx/test.gpx'
        trpts = TrackPoints(dim=2)
        trpts.create(fn)
        add_dial = DialogAddGpsTracks(trpts,parent=parent)
        add_dial.exec_()
        tr = add_dial.get_track()
        if tr and iface: # uzytkownik kliknal 'OK' i wtyczka dziala w QGIS
            print tr[0].line().wkt(), tr[1]
            tracks_layer.edit()
            contr, ti = tr[0],tr[1]
            atrs = [tracks_layer.max_id()+1, ti['rodzaj'], ti['data'], ti['autor'],
                     contr.min_time(), contr.max_time(), ti['czest'], ti['uwagi']]
            af = tracks_layer.add_feature(tr[0].line(), atr=atrs)
            if af[0]:
                tracks_layer.save()
                tracks_layer.layer.setSelectedFeatures([af[1].id()])
                iface.mapCanvas().zoomToSelected()
    else:
        QMessageBox.information(self, u'Błąd', u'Nie znaleziono warstwy "trasy"') 
                
    
def add_points(self,parent=None):
    QMessageBox.Information(self,u'Dodaj punkty',u'Metoda nie jest zaimplementowana')

def db_info(self):
    lay = Layer('trasy')
    QMessageBox.information(None, u'Informacje o bazie danych', lay.get_info())
    
def license(self):
    lay = Layer('trasy')
    QMessageBox.information(None,u'Licencja',u'(c) Miłosz Pigłas 2011-2012. Wszystkie prawa zastrzeżone\n'
                                    +u'Dystrybucja na warunkach licencji BSD\n\n'+lay.get_info())
    
def main(parent=None,iface=None,app=None):
    mw = QMainWindow(parent=parent)
    mw.setWindowTitle('AZP2-GPS')
    plugin_dialog = QFrame(parent=mw)
    mw.setCentralWidget(plugin_dialog)
    #plugin_dialog.setModal(False)
    hbox = QHBoxLayout(plugin_dialog)
    btn_add_track = QPushButton(u'Dodaj trasę',parent=plugin_dialog)
    hbox.addWidget(btn_add_track)
    btn_add_points = QPushButton(u'Dodaj punkty',parent=plugin_dialog)
    hbox.addWidget(btn_add_points)
    btn_license = QPushButton(u'Licencja',parent=plugin_dialog)
    hbox.addWidget(btn_license)
    plugin_dialog.connect(btn_add_track, SIGNAL('clicked(bool)'),partial(add_track,parent=plugin_dialog,iface=iface))
    plugin_dialog.connect(btn_add_points, SIGNAL('clicked(bool)'),partial(add_points,parent=plugin_dialog))
    plugin_dialog.connect(btn_license, SIGNAL('clicked(bool)'),license)
    #plugin_dialog.exec_()
    mw.show()
    if app:
        app.exec_()
    
if __name__ == '__main__':
    from sys import argv
    app = QApplication(argv)
    main(app=app)
