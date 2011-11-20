# -*- coding: utf-8 -*-

# qazp.py

import sys

from PyQt4.QtCore import QObject,SIGNAL, QSettings
from PyQt4.QtGui import QAction,QMainWindow,QAbstractItemView,QTableWidgetItem,QApplication
import logging

from lib.model import DaneAzp
from lib.db.postgre import PolPg
from gui.widgety.main_win import MainWindow
from gui.slownik import MiejscaSlownik,PowiatySlownik,WojewodSlownik,GminySlownik
from gui.slownik import KulturySlownik,FunkcjeSlownik,EpokiSlownik
from gui.lokalizacja import LokalizacjaDialog
from gui.informacje import InfoDialog
from gui.widgety import zest_widok
from gui.widgety.edytor_sql import EdytorSql,BladSql

class QGisPlugin(object):
    
    def __init__(self,iface):
        self.iface = iface
        
    def initGui(self):
        self.akcja = QAction("QAZP", self.iface.mainWindow())
        self.akcja.setWhatsThis("Archeologiczne Zdjecie Polski")
        self.akcja.setStatusTip("AZP")
        QObject.connect(self.akcja, SIGNAL("triggered()"), self.run)

        self.iface.addToolBarIcon(self.akcja)
        self.iface.addPluginToMenu("QAZP",self.akcja)
    
    def unload(self):
        self.iface.removePluginMenu("QAZP",self.akcja)
        self.iface.removeToolBarIcon(self.akcja)
    
    def get_ustawienia(self):
        logging.basicConfig(filename='log.txt',level=logging.INFO)
        qgis_ust = QSettings()
        logging.info(qgis_ust.applicationName())
        qgis_ust.beginGroup("/PostgreSQL/connections")
        nazwa = unicode(qgis_ust.value("selected").toString())
        logging.info(nazwa)
        host = unicode(qgis_ust.value("%s/host"%nazwa).toString())
        port = unicode(qgis_ust.value("%s/port"%nazwa).toString())
        db = unicode(qgis_ust.value("%s/database"%nazwa).toString())
        usr = unicode(qgis_ust.value("%s/username"%nazwa).toString())
        pswd = unicode(qgis_ust.value("%s/password"%nazwa).toString())
        ud =  {'db':db, 'user':usr, 'pswd':pswd, 'host':host, 'port':port}
        logging.info(str(ud))
        return ud
    
    def run(self):
        okno = OknoGlowne(self.iface.mainWindow(),self.get_ustawienia())
        okno.show()
        

class OknoGlowne(QMainWindow,MainWindow):
    
    ark_ind = -1
    nr_ind = -1
    tb_ark = []
    tb_nr = []
    tb_stan = []
    
    def __init__(self,parent=None,con_info = None):
        '''
        Inicjalizacja glownego okna aplikacji
        @param parent: widget-przodek tworzonego okna
        '''
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.tabela.setColumnCount(6)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.setSelectionMode(QAbstractItemView.SingleSelection)
        #setselectionbehavior i setselectionmode
        
        if con_info is None:
            self.con = PolPg('database','user','passwd',hn='192.168.121.1')
        else:
            self.con = PolPg(con_info['db'],con_info['user'],con_info['pswd'],hn=con_info['host'])
        self.dane = DaneAzp()
        self.dane.set_polaczenie(self.con)
        
        self.arkusz_cb.addItem("Wszystkie")
        self.tb_ark = self.dane.lista_ark()
        self.arkusz_cb.addItems(self.tb_ark)
        self.connect(self.arkusz_cb,SIGNAL('activated(int)'),self.ark_wybor)
        
        self.nrark_cb.addItem("Wszystkie")
        self.connect(self.nrark_cb,SIGNAL('activated(int)'),self.nr_wybor)
        
        self.connect(self.filtr_btn,SIGNAL('clicked()'),self.filtruj)
        self.connect(self.lokal_btn,SIGNAL('clicked()'),self.lokalizacja)
        self.connect(self.info_btn,SIGNAL('clicked()'),self.info)
        self.connect(self.miasta_akcja,SIGNAL('triggered()'),self.miasta_dialog)
        self.connect(self.powiaty_akcja,SIGNAL('triggered()'),self.pows_dialog)
        self.connect(self.wojewod_akcja,SIGNAL('triggered()'),self.wojs_dialog)
        self.connect(self.gminy_akcja,SIGNAL('triggered()'),self.gminy_dialog)
        self.connect(self.kultury_akcja,SIGNAL('triggered()'),self.kul_dialog)
        self.connect(self.funkcje_akcja,SIGNAL('triggered()'),self.fun_dialog)
        self.connect(self.epoki_akcja,SIGNAL('triggered()'),self.ep_dialog)
        
        # zestawienia
        zest_zlicz_kult_akcja = QAction(self)
        self.zest_menu.addAction(zest_zlicz_kult_akcja)
        self.connect(zest_zlicz_kult_akcja, SIGNAL('triggered()'),self.zest_zlicz_kult)
        zest_zlicz_kult_akcja.setText("Zliczaj kultury")
        uzyt_zest = QAction(self)
        self.connect(uzyt_zest,SIGNAL('triggered()'),self.nowe_zestawienie)
        self.zest_menu.addAction(uzyt_zest)
        uzyt_zest.setText("Nowe zestawienie")
        
    def nowe_zestawienie(self):    
        '''
        Wyswietla edytor polecen SQL i wykonuje polecenie wprowadzone przez uzytkownika
        '''
        edytor = EdytorSql(self)
        r = edytor.exec_()
        if r == 1:
            sql = edytor.get_tekst()
            if sql is not None:
                z = self.con.utworz_zestawienie(edytor.get_tekst())
                err = z.wykonaj()
                if err is None:
                    widok = zest_widok.ZestWidok(z,self)
                    widok.exec_()
                    z.usun_cursor()
                else:
                    widokerr = BladSql(err,self)
                    widokerr.exec_()
    
    def zest_zlicz_kult(self):
        sql = "select k.nazwa,count(*) as ile_kul from kultury_slo k right outer join materialy m on m.kultura = k.sid group by k.nazwa"    
        z = self.con.utworz_zestawienie(sql)
        z.wykonaj()
        widok = zest_widok.ZestWidok(z,self)
        widok.exec_()
        z.usun_cursor()
        
        
    def info(self):
        '''
        Wyswietla okno dialogowe z informacjami o zaznaczonym badaniu
        '''
        tr = self.tabela.currentRow()
        dial = InfoDialog(self.dane,self.tb_stan[tr])
        dial.exec_()    
        
    def lokalizacja(self):
        '''
        Wyswietla okno dialogowe z informacjami o lokalizacji zanczonego badania
        '''
        tr = self.tabela.currentRow()
        st = self.tb_stan[tr]
        lok = self.dane.lokalizacja(st)
        dial = LokalizacjaDialog(lok,self.dane,self)
        dial.exec_()
    
    def kul_dialog(self):
        '''
        Wyswietla okno dialogowe slownika kultur
        '''
        dial = KulturySlownik(self.dane,parent=self)
        dial.exec_()
        
    def fun_dialog(self):
        '''
        wyswietla slownik z funkcjami 
        '''
        dial = FunkcjeSlownik(self.dane,parent=self)
        dial.exec_()
        
    def ep_dialog(self):
        '''
        wyswietla slownik z epokami
        '''
        dial = EpokiSlownik(self.dane,parent=self)
        dial.exec_()
        
    def gminy_dialog(self):
        '''
        wyswietla slownik z gminami
        '''
        dial = GminySlownik(self.dane,parent=self)
        dial.exec_()    
        
    def miasta_dialog(self):
        '''
        wyswietla slownik z miastami
        '''
        dial = MiejscaSlownik(self.dane,parent=self)
        dial.exec_()
        
    def pows_dialog(self):
        '''
        wyswietla slownik z powiatami
        '''
        dial = PowiatySlownik(self.dane,parent=self)
        dial.exec_()
        
    def wojs_dialog(self):
        '''
        wyswietla dialog z wojewodztwami
        '''
        dial = WojewodSlownik(self.dane,parent=self)
        dial.exec_()
        
    def ark_wybor(self,x):
        if x > 0 and x != self.ark_ind:
            self.ark_ind = x
            self.tb_nr = self.dane.lista_nrark(self.tb_ark[x-1])
            self.nrark_cb.clear()
            self.nrark_cb.addItem("Wszystkie")
            self.nrark_cb.addItems(self.tb_nr)
        elif x == 0:
            self.ark_ind = -1
            
    def nr_wybor(self,x):
        if x > 0:
            self.nr_ind = x
        elif x == 0:
            self.nr_ind = -1
    
    def __item(self,var):
        #print var
        #x = QApplication.translate(str(var), str(var), None,QApplication.UnicodeUTF8)
        if isinstance(var,unicode):
            return QTableWidgetItem(var)
        else:
            return QTableWidgetItem(QApplication.translate(str(var), str(var), None,QApplication.UnicodeUTF8))        
            
    def dodaj_stanowisko(self,w,s):
        self.tabela.setItem(w,0,self.__item(s.arkusz))
        self.tabela.setItem(w,1,self.__item(s.nr_ark))
        self.tabela.setItem(w,2,self.__item(s.miejsce))
        self.tabela.setItem(w,3,self.__item(s.nr_miejsce))
        self.tabela.setItem(w,4,self.__item(s.data))
        self.tabela.setItem(w,5,self.__item(s.autor))
            
    def filtruj(self):
        a,n = -1,-1
        if self.ark_ind > 0:
            a = self.tb_ark[self.ark_ind-1]
        else:
            return
        if self.nr_ind > 0:
            n = self.tb_nr[self.nr_ind-1]
        if a > -1:
            self.tb_stan = self.dane.stanowiska(a,n)
        self.tabela.setRowCount(len(self.tb_stan))
        self.tabela.setSortingEnabled(False)
        for (si,s) in enumerate(self.tb_stan):
            self.dodaj_stanowisko(si,s)
        self.tabela.resizeColumnsToContents()
        if len(self.tb_stan) > 0:
            self.tabela.selectRow(0)
        
    
if __name__ == "__main__":        
    app = QApplication(sys.argv)
    okno = OknoGlowne()
    okno.show()
    app.exec_()