# -*- coding: utf-8 -*-

# qazp.py

import sys

from PyQt4.QtCore import QObject,SIGNAL, QSettings
from PyQt4.QtGui import QAction,QMainWindow,QAbstractItemView,QTableWidgetItem,QApplication,QHeaderView,QMessageBox
from PyQt4.QtGui import QInputDialog, QPrintDialog,QFileDialog

from lib.model import DaneAzp
from lib.db.postgre import PolPg
from lib.db.azpsqlite import SqliteDb
from gui.widgety.main_win import MainWindow
from gui.slownik import MiejscaSlownik,PowiatySlownik,WojewodSlownik,GminySlownik
from gui.slownik import KulturySlownik,FunkcjeSlownik,EpokiSlownik
from gui.lokalizacja import LokalizacjaDialog
from gui.informacje import InfoDialog
from gui.widgety import zest_widok
from gui.widgety.edytor_sql import EdytorSql,BladSql
from lib.dokument import Dokument

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
    
    def run(self):
        okno = OknoGlowne(self.iface.mainWindow(),True)
        okno.show()
        

class OknoGlowne(QMainWindow,MainWindow):
    
    ark_ind = -1
    nr_ind = -1
    tb_ark = []
    tb_nr = []
    tb_stan = []
    
    def __init__(self,parent=None,plugin=False):
        '''
        Inicjalizacja glownego okna aplikacji
        @param parent: widget-przodek tworzonego okna
        '''
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.tabela.setColumnCount(6)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabela.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.tabela.setHorizontalHeaderItem(0,self.__item("Arkusz"))
        self.tabela.setHorizontalHeaderItem(1,self.__item("Numer na arkuszu"))
        self.tabela.setHorizontalHeaderItem(2,self.__item("Miejscowość"))
        self.tabela.setHorizontalHeaderItem(3,self.__item("Nr w miejscowości"))
        self.tabela.setHorizontalHeaderItem(4,self.__item("Data"))
        self.tabela.setHorizontalHeaderItem(5,self.__item("Autor badań"))
        #setselectionbehavior i setselectionmode
        
        #if con_info is None:
        #    self.con = PolPg('azp2','gis','gis',hn='192.168.121.1')
        #else:
        #    self.con = PolPg(con_info['db'],con_info['user'],con_info['pswd'],hn=con_info['host'])
        con_info = None
        if plugin:
            con_info = self.get_ustawienia()
        self.con = self.get_con(con_info)
        self.connect(self.arkusz_cb,SIGNAL('activated(int)'),self.ark_wybor)
        self.set_dane(self.con)
        #self.nrark_cb.addItem("Wszystkie")
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
        self.connect(self.typdb_pg,SIGNAL('toggled(bool)'),self.wybor_pg)
        self.connect(self.typdb_spat,SIGNAL('toggled(bool)'),self.wybor_spat)
        
        self.typdb_pg.setCheckable(True)
        self.typdb_spat.setCheckable(True)
        if con_info and con_info['typdb'] == 'spatialite':
            self.typdb_spat.setChecked(True)
        elif con_info and con_info['typdb'] == 'postgis':
            self.typdb_pg.setChecked(True)
        else:
            self.typdb_spat.setChecked(True)
        
        # zestawienia
        zest_zlicz_kult_akcja = QAction(self)
        self.zest_menu.addAction(zest_zlicz_kult_akcja)
        self.connect(zest_zlicz_kult_akcja, SIGNAL('triggered()'),self.zest_zlicz_kult)
        zest_zlicz_kult_akcja.setText("Zliczaj kultury")
        
        zest_stan_gmina_akcja = QAction(self)
        self.zest_menu.addAction(zest_stan_gmina_akcja)
        self.connect(zest_stan_gmina_akcja, SIGNAL('triggered()'),self.zest_stan_gmina)
        zest_stan_gmina_akcja.setText("Stanowiska w gminie ...")
        zest_stan_gmina_akcja.setToolTip(u'Wyświetla stanowiska w wybranej gminie')
        
        zest_stan_miej_akcja = QAction(self)
        self.zest_menu.addAction(zest_stan_miej_akcja)
        self.connect(zest_stan_miej_akcja, SIGNAL('triggered()'),self.zest_stan_miej)
        zest_stan_miej_akcja.setText(u"Stanowiska w miejscowości ...")
        zest_stan_miej_akcja.setToolTip(u'Wyświetla stanowiska w wybranej miejscowości')
        
        zest_stan_ark_akcja = QAction(self)
        self.zest_menu.addAction(zest_stan_ark_akcja)
        self.connect(zest_stan_ark_akcja, SIGNAL('triggered()'),self.zest_stan_ark)
        zest_stan_ark_akcja.setText(u"Stanowiska na arkuszu ...")
        zest_stan_ark_akcja.setToolTip(u'Wyświetla stanowiska na wybranym arkuszu')
        
        zest_stan_kultura_akcja = QAction(self)
        self.zest_menu.addAction(zest_stan_kultura_akcja)
        self.connect(zest_stan_kultura_akcja, SIGNAL('triggered()'),self.zest_stan_kul)
        zest_stan_kultura_akcja.setText(u"Stanowiska z kulturą ...")
        zest_stan_kultura_akcja.setToolTip(u'Wyświetla stanowiska z wybraną kulturą')
        
        zest_stan_epoka_akcja = QAction(self)
        self.zest_menu.addAction(zest_stan_epoka_akcja)
        self.connect(zest_stan_epoka_akcja, SIGNAL('triggered()'),self.zest_stan_epoka)
        zest_stan_epoka_akcja.setText(u"Stanowiska z epoką ...")
        zest_stan_epoka_akcja.setToolTip(u'Wyświetla stanowiska z wybraną epoką')
        
        zest_stan_fun_akcja = QAction(self)
        self.zest_menu.addAction(zest_stan_fun_akcja)
        self.connect(zest_stan_fun_akcja, SIGNAL('triggered()'),self.zest_stan_fun)
        zest_stan_fun_akcja.setText(u"Stanowiska z funkcją ...")
        zest_stan_fun_akcja.setToolTip(u'Wyświetla stanowiska z wybraną funkcją')
        
        self.zest_menu.addSeparator()
        zest_ark_grupy_akcja = QAction(self)
        self.zest_menu.addAction(zest_ark_grupy_akcja)
        self.connect(zest_ark_grupy_akcja, SIGNAL('triggered()'),self.zest_ark_grupy)
        zest_ark_grupy_akcja.setText(u"Zliczaj wg arkusza")
        zest_ark_grupy_akcja.setToolTip(u'Wyświetla liczbę stanowisk na arkuszach')
        
        zest_miej_grupy_akcja = QAction(self)
        self.zest_menu.addAction(zest_miej_grupy_akcja)
        self.connect(zest_miej_grupy_akcja, SIGNAL('triggered()'),self.zest_miej_grupy)
        zest_miej_grupy_akcja.setText(u"Zliczaj wg miejscowości ...")
        zest_miej_grupy_akcja.setToolTip(u'Wyświetla liczbę stanowisk w miejscowościach')
        
        zest_stan_bezlok_akcja = QAction(self)
        self.zest_menu.addAction(zest_stan_bezlok_akcja)
        self.connect(zest_stan_bezlok_akcja, SIGNAL('triggered()'),self.zest_stan_bezlok)
        zest_stan_bezlok_akcja.setText(u"Stanowiska bez lokalizacji ...")
        
        uzyt_zest = QAction(self)
        self.connect(uzyt_zest,SIGNAL('triggered()'),self.nowe_zestawienie)
        self.zest_menu.addAction(uzyt_zest)
        uzyt_zest.setText("Nowe zestawienie")
        
        # pomoc
        lic_akcja = QAction(self)
        self.pomoc_menu.addAction(lic_akcja)
        self.connect(lic_akcja, SIGNAL('triggered()'),self._licencja)
        lic_akcja.setText('Licencja')
        
        baza_info_akcja = QAction(self)
        self.pomoc_menu.addAction(baza_info_akcja)
        self.connect(baza_info_akcja, SIGNAL('triggered()'),self._baza_info)
        baza_info_akcja.setText('Informacje o bazie')    
        if not self.con.geom:
            QMessageBox.information(self, 'Wersja', u'Uwaga! Z braku wszystkich wymaganych modułów dodawanie nowych lokalizacji jest niemożliwe')    
    
        druk_akcja = QAction(self)
        self.pomoc_menu.addAction(druk_akcja)
        self.connect(druk_akcja, SIGNAL('triggered()'),self._test_druk)
        druk_akcja.setText("Test druku")
    
    def _test_druk(self):
        nazwa = QFileDialog.getSaveFileName(self)
        dok = Dokument()
        dok.dodaj_akapit(u"Przykładowy akapit")
        dok.dodaj_tabele([['abc','de','efgh','ixxx','jklm','nop'],['abc','dexxx','efgh','i','jklm','nop'],['abc','dexx','efgh','ix','jklm','xxnop']])
        dok.zapisz_pdf(nazwa)
        #self.wydruk = Wydruk()
        #pd = QPrintDialog(self)
        #pd.connect(pd, SIGNAL('accepted(QPrinter *)'),self._druk_fun)
        #pd.exec_()
    
    def _druk_fun(self, printer):
        self.wydruk.drukuj(printer)    
        
    def _baza_info(self):
        info = 'Baza: %(src)s\n Liczba lokalizacji w bazie: %(lok)s\nLiczba stanowisk w bazie: %(stan)s' % self.con.statystyka() 
        QMessageBox.information(self,'Informacje o bazie',info)   
        
    def _licencja(self):
        QMessageBox.information(self, 'Licencja', u'(c) Miłosz Pigłas 2011-2012. Wszystkie prawa zastrzeżone\nDystrybucja na warunkach licencji BSD')
    
    def get_ustawienia(self):
        qgis_ust = QSettings()
        ud = {}
        qgis_ust.beginGroup("/QAzp")
        if qgis_ust.contains("typdb"):
            ud['typdb'] = unicode(qgis_ust.value('typdb').toString())
        else:
            ud['typdb']='spatialite'
            qgis_ust.setValue('typdb','spatialite')
        qgis_ust.endGroup()
        if ud['typdb'] == 'spatialite':
            qgis_ust.beginGroup('/Spatialite/connections')
            nazwa = unicode(qgis_ust.value("selected").toString())
            if '@' in nazwa:
                nazwa = nazwa.split('@')[0]
            plik = unicode(qgis_ust.value("%s/sqlitepath"%nazwa).toString())
            ud['plik'] = plik
        elif ud['typdb'] == 'postgis':
            qgis_ust.beginGroup("/PostgreSQL/connections")
            ud['nazwa'] = unicode(qgis_ust.value("selected").toString())
            ud['host'] = unicode(qgis_ust.value("%s/host"%nazwa).toString())
            ud['port'] = unicode(qgis_ust.value("%s/port"%nazwa).toString())
            ud['db'] = unicode(qgis_ust.value("%s/database"%nazwa).toString())
            ud['user'] = unicode(qgis_ust.value("%s/username"%nazwa).toString())
            ud['pswd'] = unicode(qgis_ust.value("%s/password"%nazwa).toString())
            
        return ud
    
    def get_con(self,con_info=None):
        if not con_info:
            plik_db = QInputDialog.getText(self,"Baza danych","Podaj lokalizacje bazy danych",
                                           text="/home/milosz/archeocs/azp2/azp2_2.db")
            if plik_db[1]:
                return SqliteDb(str(plik_db[0]))
            return SqliteDb("/home/milosz/archeocs/azp2/azp3.db")
        else:
            if con_info['typdb'] == 'spatialite' and con_info.has_key('plik'):
                return SqliteDb(con_info['plik'])
            elif con_info['typdb'] == 'postgis' and con_info.has_key('db'):
                return PolPg(con_info['db'],con_info['user'],con_info['pswd'],hn=con_info['host'])
        return None
    
    def set_dane(self,con):
        self.dane = DaneAzp()
        self.dane.set_polaczenie(con)
        self.arkusz_cb.clear()
        self.arkusz_cb.addItem("Wszystkie")
        dark = self.dane.lista_ark()
        if dark[0]:
            self.tb_ark = dark[1]
            self.arkusz_cb.addItems(self.tb_ark)
            self.nrark_cb.clear()
            self.nrark_cb.addItem("Wszystkie")
        else:
            QMessageBox.critical(self,u"Błąd",u"Wystąpił błąd. Sprawdź czy baza danych jest prawidłowa\nInformacja o błędzie: "+
                             dark[2],"OK")
        
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
        sql = """select k.nazwa,count(*) as ile_kul from  materialy m join kultury_slo k on 
                    m.kultura = k.sid where m.kultura > 0 group by k.nazwa"""   
        z = self.con.utworz_zestawienie(sql)
        z.wykonaj()
        widok = zest_widok.ZestWidok(z,self)
        widok.exec_()
        z.usun_cursor()
        
    def zest_stan_gmina(self):
        slow = self.dane.gminy()
        ret = QInputDialog.getItem(self, u"Wybierz gminę", u"Wybierz gminę z listy i kliknij OK", slow.lista(), editable=False)
        if ret[1]:
            sql = """select m.nazwa, l.nr_miejscowosc, l.arkusz||'/'||l.nr_arkusz as AZP, s.data, s.autor 
                    from stanowiska s join lokalizacje l on s.lokalizacja = l.lid join
                    miasta_slo m on l.miejscowosc = m.sid where l.gmina=%d"""%slow.nazwa_sid(str(ret[0]))
            z = self.con.utworz_zestawienie(sql)
            z.wykonaj()
            widok = zest_widok.ZestWidok(z,self)
            widok.setWindowTitle(u'Stanowiska w gminie')
            widok.exec_()
            z.usun_cursor()
    
    def zest_stan_miej(self):
        slow = self.dane.miasta()
        ret = QInputDialog.getItem(self, u"Wybierz miejscowość", u"Wybierz miejscowość z listy i kliknij OK", slow.lista(), editable=False)
        if ret[1]:
            sql = """select m.nazwa, l.nr_miejscowosc, l.arkusz||'/'||l.nr_arkusz as AZP, s.data, s.autor 
                    from stanowiska s join lokalizacje l on s.lokalizacja = l.lid join
                    miasta_slo m on l.miejscowosc = m.sid where l.miejscowosc=%d"""%slow.nazwa_sid(str(ret[0]))
            z = self.con.utworz_zestawienie(sql)
            z.wykonaj()
            widok = zest_widok.ZestWidok(z,self)
            widok.setWindowTitle(u'Stanowiska w miejscowości')
            widok.exec_()
            z.usun_cursor()
    
    def zest_stan_ark(self):
        ret = QInputDialog.getText(self, u'Arkusz AZP', u'Podaj numer arkusza i kliknij OK')
        if ret[1]:
            sql = """select m.nazwa, l.nr_miejscowosc, l.arkusz||'/'||l.nr_arkusz as AZP, s.data, s.autor 
                    from stanowiska s join lokalizacje l on s.lokalizacja = l.lid join
                    miasta_slo m on l.miejscowosc = m.sid where l.arkusz='%s'"""%str(ret[0])
            z = self.con.utworz_zestawienie(sql)
            z.wykonaj()
            widok = zest_widok.ZestWidok(z,self)
            widok.setWindowTitle(u'Stanowiska na arkuszu')
            widok.exec_()
            z.usun_cursor()
            
    def zest_stan_kul(self):
        slow = self.dane.kultury()
        ret = QInputDialog.getItem(self, u"Wybierz kulturę", u"Wybierz kulturę z listy i kliknij OK", slow.lista(), editable=False)
        if ret[1]:
            sql = """select k.nazwa as KULTURA, c.nazwa as MIEJSCOWOŚĆ , l.nr_miejscowosc, l.arkusz||'/'||l.nr_arkusz as AZP, s.data, s.autor 
                    from stanowiska s join lokalizacje l on s.lokalizacja = l.lid join materialy m on s.sid = m.stanowisko
                    join kultury_slo k on k.sid = m.kultura join miasta_slo c on l.miejscowosc = 
                    c.sid where m.kultura=%d"""%slow.nazwa_sid(str(ret[0]))
            z = self.con.utworz_zestawienie(sql)
            z.wykonaj()
            widok = zest_widok.ZestWidok(z,self)
            widok.setWindowTitle(u'Stanowiska z kulturą')
            widok.exec_()
            z.usun_cursor()
            
    def zest_stan_epoka(self):
        slow = self.dane.epoki()
        ret = QInputDialog.getItem(self, u"Wybierz epokę", u"Wybierz epokę z listy i kliknij OK", slow.lista(), editable=False)
        if ret[1]:
            sql = """select e.nazwa as EPOKA, c.nazwa as MIEJSCOWOŚĆ , l.nr_miejscowosc, l.arkusz||'/'||l.nr_arkusz as AZP, s.data,
                     s.autor 
                    from stanowiska s join lokalizacje l on s.lokalizacja = l.lid join materialy m on s.sid = m.stanowisko
                    join epoki_slo e on e.sid = m.epoka join miasta_slo c on l.miejscowosc = 
                    c.sid where m.epoka=%d"""%slow.nazwa_sid(str(ret[0]))
            z = self.con.utworz_zestawienie(sql)
            z.wykonaj()
            widok = zest_widok.ZestWidok(z,self)
            widok.setWindowTitle(u'Stanowiska z epoką')
            widok.exec_()
            z.usun_cursor()
            
    def zest_stan_fun(self):
        slow = self.dane.funkcje()
        ret = QInputDialog.getItem(self, u"Wybierz funkcję", u"Wybierz funkcję z listy i kliknij OK", slow.lista(), editable=False)
        if ret[1]:
            sql = """select f.nazwa as FUNKCJA, c.nazwa as MIEJSCOWOŚĆ , l.nr_miejscowosc, l.arkusz||'/'||l.nr_arkusz as AZP, s.data,
                     s.autor 
                    from stanowiska s join lokalizacje l on s.lokalizacja = l.lid join materialy m on s.sid = m.stanowisko
                    join funkcje_slo f on f.sid = m.funkcja join miasta_slo c on l.miejscowosc = 
                    c.sid where m.funkcja=%d"""%slow.nazwa_sid(str(ret[0]))
            z = self.con.utworz_zestawienie(sql)
            z.wykonaj()
            widok = zest_widok.ZestWidok(z,self)
            widok.setWindowTitle(u'Stanowiska z funkcją')
            widok.exec_()
            z.usun_cursor()
            
    def zest_ark_grupy(self):
        sql = """select count(*) as 'LICZBA STANOWISK', l.arkusz as ARKUSZ from stanowiska s join lokalizacje l on s.lokalizacja = l.lid
                    group by l.arkusz order by l.arkusz """
        z = self.con.utworz_zestawienie(sql)
        z.wykonaj()
        widok = zest_widok.ZestWidok(z,self)
        widok.setWindowTitle(u'LICZBA STANOWISK WG ARKUSZA')
        widok.exec_()
        z.usun_cursor()
        
    def zest_miej_grupy(self):
        sql = u"""select count(*) as 'LICZBA STANOWISK', m.nazwa as MIEJSCOWOŚĆ from stanowiska s join lokalizacje l on 
                    s.lokalizacja = l.lid join miasta_slo m on l.miejscowosc = m.sid group by m.nazwa order by m.nazwa """
        z = self.con.utworz_zestawienie(sql)
        z.wykonaj()
        widok = zest_widok.ZestWidok(z,self)
        widok.setWindowTitle(u'LICZBA STANOWISK WG MIEJSCOWOŚCI')
        widok.exec_()
        z.usun_cursor()
        
    def zest_stan_bezlok(self):
        sql = u""" select miejscowosc as MIEJSCOWOŚĆ, nr_miejscowosc AS NUMER, arkusz||'/'||nr_arkusz as 
                AZP, data from stanowiska where lokalizacja is NULL """
        z = self.con.utworz_zestawienie(sql)
        z.wykonaj()
        widok = zest_widok.ZestWidok(z,self)
        widok.setWindowTitle(u'STANOWISKA BEZ LOKALIZACJI')
        widok.exec_()
        z.usun_cursor()
                
    def set_typdb(self,typ):
        qgis_ust = QSettings()
        qgis_ust.beginGroup('/QAzp')
        qgis_ust.setValue('typdb',typ)
        qgis_ust.endGroup()   
        #self.con = self.get_con(self.get_ustawienia())
        #self.set_dane(self.con) 
    
    def wybor_pg(self,zazn):
        if zazn:
            self.set_typdb('postgis')
            self.typdb_spat.setChecked(False)
    
    def wybor_spat(self,zazn):
        if zazn:
            self.set_typdb('spatialite')
            self.typdb_pg.setChecked(False)  
        
    def info(self):
        '''
        Wyswietla okno dialogowe z informacjami o zaznaczonym badaniu
        '''
        tr = self.tabela.currentRow()
        stanowisko = self.tb_stan[tr]
        if stanowisko.lokalizacja:
            dial = InfoDialog(self.dane,stanowisko)
            dial.exec_()  
        else:
            QMessageBox.critical(self,u"Nie mogę wyświetlić danych",u"Stanowisko nie ma określonej lokalizacji.","OK")  
        
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
            dnr = self.dane.lista_nrark(self.tb_ark[x-1])
            if dnr[0]:
                self.tb_nr = dnr[1]
                self.nrark_cb.clear()
                self.nrark_cb.addItem("Wszystkie")
                self.nrark_cb.addItems(self.tb_nr)
            else:
                QMessageBox.critical(self,u"Błąd",u"Wystąpił błąd. Sprawdź czy baza danych jest prawidłowa\nInformacja o błędzie: "+
                             dnr[2],"OK")
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