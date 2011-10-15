# -*- coding: utf-8 -*-

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QComboBox,QSpinBox,QDialog,QVBoxLayout,QTabWidget,QDialogButtonBox,QApplication
from widgety.infotab import InfoTab
from widgety.tabelatab import TabelaTab
import uzytki

class MaterialyTab(TabelaTab):
    def __init__(self,stan,dane): # epoki_dict - slownik epok, kultury_dict - slownik kultur, fazy_dict - slownik funkcji
        TabelaTab.__init__(self)
        self.set_slowniki(dane.epoki(),dane.kultury(),dane.funkcje())
        self.fakty = dane.fakty(stan)
        self.dane = dane
        self.stan = stan
        for fakt in self.fakty:
            self.wstaw_fakt(fakt)
    
    def wstaw_fakt(self,fakt):
        #print unicode(fakt)
        self.dodajWiersz([fakt.epoka_nazwa,fakt.kultura_nazwa,fakt.funkcja_nazwa,fakt.cer,fakt.kam,fakt.met])   
    
    def set_slowniki(self,ed,kd,fd):
        self.epoki_dict = ed
        self.epoka_cb.addItems(ed.lista())
        self.kultury_dict = kd
        self.kul_cb.addItems(kd.lista())
        self.fazy_dict = fd
        self.fun_cb.addItems(fd.lista())
        
    def dodajPola(self,pasek): # metoda wywolywana w konstruktorze przodka (TableTab)
        self.epoka_cb = pasek.dodaj_widget(QComboBox(),prefsz=80)
        self.epoka_cb.addItem('Epoki')
        self.epoka_cb.addItem(uzytki.to_unicode('Nieokreślona'))
        
        self.kul_cb = pasek.dodaj_widget(QComboBox(),prefsz=80)
        self.kul_cb.addItem('Kultury')
        self.kul_cb.addItem(uzytki.to_unicode('Nieokreślona'))
        
        self.fun_cb = pasek.dodaj_widget(QComboBox(),prefsz=80)
        self.fun_cb.addItem('Funkcje')
        self.fun_cb.addItem(uzytki.to_unicode('Nieokreślona'))
        
        self.ceram_sb = pasek.dodaj_widget(QSpinBox(),prefsz=40)
        self.kam_sb = pasek.dodaj_widget(QSpinBox(),prefsz=40)
        self.met_sb = pasek.dodaj_widget(QSpinBox(),prefsz=40)
        
    def _nieokresl(self,i,klucz,slo):
        if i < 2:
            return 0
        else:
            return slo.nazwa_sid(klucz)
            
    def nieokresl(self,cb,slo):
        i = cb.currentIndex()
        if i < 2:
            return (0,u'Nieokreślona')
        else:
            nazwa = unicode(cb.currentText())
            slow_id = slo.nazwa_sid(nazwa)
            return (slow_id,nazwa)
        
    def zatwierdzZmiany(self,i,nowy):
        if nowy:
            nowy_fakt = self.dane.nowy_fakt(self.stan)
            tup = self.nieokresl(self.epoka_cb,self.epoki_dict)
            nowy_fakt.epoka_nazwa = tup[1]
            nowy_fakt.epoka = tup[0]
            tup = self.nieokresl(self.kul_cb,self.kultury_dict)
            nowy_fakt.kultura_nazwa = tup[1]
            nowy_fakt.kultura = tup[0]
            tup = self.nieokresl(self.fun_cb,self.fazy_dict)
            nowy_fakt.funkcja_nazwa = tup[1]
            nowy_fakt.funkcja = tup[0]
            nowy_fakt.cer = self.ceram_sb.value()
            nowy_fakt.kam = self.kam_sb.value()
            nowy_fakt.met = self.met_sb.value()
            self.fakty.append(nowy_fakt)
            self.dodajWiersz([nowy_fakt.epoka_nazwa,nowy_fakt.kultura_nazwa,nowy_fakt.funkcja_nazwa,nowy_fakt.cer,nowy_fakt.kam,nowy_fakt.met])
        else:
            mod_fakt = self.fakty[i]
            tup = self.nieokresl(self.epoka_cb, self.epoki_dict)
            mod_fakt.epoka_nazwa = tup[1]
            mod_fakt.epoka=tup[0]
            tup = self.nieokresl(self.kul_cb,self.kultury_dict)
            mod_fakt.kultura_nazwa = tup[1]
            mod_fakt.kultura = tup[0]
            tup = self.nieokresl(self.fun_cb,self.fazy_dict)
            mod_fakt.funkcja_nazwa = tup[1]
            mod_fakt.funkcja = tup[0]
            mod_fakt.cer = self.ceram_sb.value()
            mod_fakt.kam = self.kam_sb.value()
            mod_fakt.met = self.met_sb.value()
            mod_fakt.czy_mod = True
            self.fakty[i] = mod_fakt
            self.zmienWiersz(i, [mod_fakt.epoka_nazwa,mod_fakt.kultura_nazwa,mod_fakt.funkcja_nazwa,mod_fakt.cer,mod_fakt.kam,mod_fakt.met])
            
            
    def zapisz(self):
        for fakt in self.fakty:
            if fakt.czy_nowy:
                print 'nowy ',unicode(fakt)
                print fakt.zapisz()
            elif fakt.czy_mod:
                print 'mod', unicode(fakt)
                print fakt.zapisz()
        
    def aktywuj_edytor(self,i,wiersz):
        '''
        Aktualizuje pola combo, ktore sa uzywane do edycji tabeli
        @param i: numer wiersza
        @param wiersz: tabela reprezentujaca wiersz. jesli jest rowna None to znaczy ze dodawany jest nowy wiersz
        '''
        if wiersz is not None:
            ed_pole = unicode(wiersz[0].text())
            if ed_pole != u'Nieokreślona':
                self.epoka_cb.setCurrentIndex(self.epoki_dict.nazwa_ind(unicode(wiersz[0].text()))+2)
            else:
                self.epoka_cb.setCurrentIndex(1)
            ku = unicode(wiersz[1].text())
            if ku != u'Nieokreślona':    
                self.kul_cb.setCurrentIndex(self.kultury_dict.nazwa_ind(unicode(wiersz[1].text()))+2)
            else:
                self.kul_cb.setCurrentIndex(1)
            fu = unicode(wiersz[2].text())
            if fu != u'Nieokreślona':    
                self.fun_cb.setCurrentIndex(self.fazy_dict.nazwa_ind(unicode(wiersz[2].text()))+2)
            else:
                self.fun_cb.setCurrentIndex(1)    
            self.ceram_sb.setValue(int(str(wiersz[3].text())))
            self.kam_sb.setValue(int(str(wiersz[4].text())))
            self.met_sb.setValue(int(str(wiersz[5].text())))
        else:
            self.epoka_cb.setCurrentIndex(0)
            self.kul_cb.setCurrentIndex(0)
            self.fun_cb.setCurrentIndex(0)
            self.ceram_sb.setValue(0)
            self.kam_sb.setValue(0)
            self.met_sb.setValue(0)

class PolozenieTab(InfoTab):
    """ self.jedn = td[2].decode('utf-8')
            self.morze,self.plaza,self.mierz,self.skarpa,self.wal,self.woda,self.terden = zm[td[3]],zm[td[4]],zm[td[5]],zm[td[6]],zm[td[7]],zm[td[8],zm[td[9]]
            self.ternad,self.terwyz,self.dnod,self.stokd,self.krawd,self.rown,self.fal = zm[td[10]],zm[td[11]],zm[td[12]],zm[td[13]],zm[td[14]],zm[td[15]],zm[td[16]]
            self.pagor,self.gorz = zm[td[17]],zm[td[18]]"""
    def __init__(self,polo):
        InfoTab.__init__(self,2,polo)
        self.jedn_txt = self.dodaj_txt("Jednostka",polo.jedn,nazwa="jedn")
        self.morze_cb = self.dodaj_combo("W morzu",polo.morze,nazwa="morze")
        self.plaza_cb = self.dodaj_combo("Plaża",polo.plaza,nazwa="plaza")
        self.mierze_cb = self.dodaj_combo("Mierzeja",polo.mierz,nazwa="mierz")
        self.skarpa_cb = self.dodaj_combo("Skarpa",polo.skarpa,nazwa="skarpa")
        self.wal_cb = self.dodaj_combo("Wał wydmowy",polo.wal,nazwa="wal")
        self.woda_cb = self.dodaj_combo("W wodzie",polo.woda,nazwa="woda")
        self.terden_cb = self.dodaj_combo("Ter. denna",polo.terden,nazwa="terden")
        self.ternad_cb = self.dodaj_combo("Ter. nadzalewowa",polo.ternad,nazwa="ternad")
        self.terwyz_cb = self.dodaj_combo("Ter. wyższa",polo.terwyz,nazwa="terwyz")
        self.dnod_cb = self.dodaj_combo("Dno doliny",polo.dnod,nazwa="dnod")
        self.stokd_cb = self.dodaj_combo("Stok doliny",polo.stokd,nazwa="stokd")
        self.krawd_cb = self.dodaj_combo("Krawędź doliny",polo.krawd,nazwa="krawd")
        self.rown_cb = self.dodaj_combo("Równina",polo.rown,nazwa="rown")
        self.fal_cb = self.dodaj_combo("Obsz. falisty",polo.fal,nazwa="fal")
        self.pagor_cb = self.dodaj_combo("Obsz. pagórkowaty",polo.pagor,nazwa="pagor")
        self.gorz_cb = self.dodaj_combo("Obsz. górzysty",polo.gorz,nazwa="gorz")
        
class EkspozycjaTab(InfoTab):
    def __init__(self,eksp):
        InfoTab.__init__(self,2,eksp)
        self.eksp_cb = self.dodaj_combo("Eksponowany",eksp.czy_eksp,nazwa="czy_eksp")
        self.kraw_cb = self.dodaj_combo("Krawędź,stok",eksp.kraw,nazwa="kraw")
        self.sfal_cb = self.dodaj_combo("Sfałdowanie",eksp.sfal,nazwa="sfal")
        self.cypel_cb = self.dodaj_combo("Cypel wybitny",eksp.cypel,nazwa="cypel")
        self.wal_cb = self.dodaj_combo("Wał, garb",eksp.wal,nazwa="wal")
        self.okrez_cb = self.dodaj_combo("Wyniesienie okrężne",eksp.okrez,nazwa="okrez")
        self.stok_cb = self.dodaj_combo("Podstawa stoku",eksp.stok,nazwa="stok")
        self.dolina_cb = self.dodaj_combo("Dolina, jar",eksp.dolina,nazwa="dolina")
        self.kotl_cb = self.dodaj_combo("Kotlinka",eksp.kotl,nazwa="kotl")
        self.jask_cb = self.dodaj_combo("Jaskinia",eksp.jask,nazwa="jask")
        self.szczeg_txt = self.dodaj_txt("Forma szczególna", eksp.szczegolna, "szczegolna")
        
class TerenTab(InfoTab):
    #self.orne,self.sad,self.torf,self.nieuz,self.park,self.laka = zm[td[2]],zm[td[3]],zm[td[4]],zm[td[5]],zm[td[6]],zm[td[7]]
    # self.bagno,self.las,self.woda,self.zab,self.niezab,self.srezab = zm[td[8]],zm[td[9]],zm[td[10]],zm[td[11]],zm[td[12],zm[td[13]]
    def __init__(self,ter):
        InfoTab.__init__(self,2,ter)
        self.pole_cb = self.dodaj_combo("Pole orne",ter.orne,nazwa="orne")
        self.sad_cb = self.dodaj_combo("Sad",ter.sad,nazwa="sad")
        self.torf_cb = self.dodaj_combo("Torfowisko",ter.torf,nazwa="torf")
        self.nieuz_cb = self.dodaj_combo("Nieużytek",ter.nieuz,nazwa="nieuz")
        self.park_cb = self.dodaj_combo("Park",ter.park,nazwa="park")
        self.laka_cb = self.dodaj_combo("Łąka",ter.laka,nazwa="laka")
        self.bagno_cb = self.dodaj_combo("Bagno",ter.bagno,nazwa="bagno")
        self.las_cb = self.dodaj_combo("Las",ter.las,nazwa="las")
        self.woda_cb = self.dodaj_combo("W wodzie",ter.woda,nazwa="woda")
        self.zab_cb = self.dodaj_combo("Zabudowany",ter.zab,nazwa="zab")
        self.niezab_cb = self.dodaj_combo("Niezabudowany",ter.niezab,nazwa="niezab")
        self.srezab_cb = self.dodaj_combo("Średniozabudowany",ter.srezab,nazwa="srezab")
        self.blizsze_txt = self.dodaj_txt("Określenie bliższe", ter.bliz, nazwa="bliz")

class ObszarTab(InfoTab):
    #obserwacja,orne,nasycenie,gestosc, powierzchnia,oid
    def __init__(self,obszar):
        InfoTab.__init__(self,1,obszar)
        self.obser_cb = self.dodaj_combo("Obserwacja", obszar.obser, [u'Nieokreślona',u'Utrudniona',u'Bez przeszkód'], nazwa="obser")
        self.pole_cb = self.dodaj_combo("Pole", obszar.pole, [u'Nieokreślone',u'Otwarte',u'Zamknięte'], nazwa="pole")
        self.nasyc_cb = self.dodaj_combo("Nasycenie", obszar.nasyc, [u'Nieokreślone',u'Równomierne',u'Nierównomierne'], nazwa="nasyc")
        self.gest_cb = self.dodaj_combo("Gęstość", obszar.gest, [u'Nieokreślona',u'Mała',u'Średnia',u'Duża'], nazwa="gest")
        self.powierz_cb = self.dodaj_combo("Powierzchnia", obszar.powierz, [u'Nieokreślona',u'< 1 a','1a -0,5ha',u'0,5ha -1ha',u'1ha -5ha',u'5ha -15ha','15ha <'], nazwa="powierz")
        self.centr_cb = self.dodaj_combo("Rozłożenie",obszar.centr,[u'Nieokreślone',u'Jednocentryczne','Wielocentryczne','Dekoncentryczne'],nazwa="centr")

class WnioskiTab(InfoTab):
    
    def __init__(self,wnioski):
        InfoTab.__init__(self,1,wnioski)
        self.wartosc = self.dodaj_combo("Wartość",wnioski.wartosc,[u'Nieokreślona',u'Mała',u'Duża'],nazwa="wartosc")
        self.inwent = self.dodaj_combo("Inwentaryzacja",wnioski.inwent,nazwa="inwent")
        self.interwencja = self.dodaj_combo("Interwencja",wnioski.interw,nazwa="interw")
        self.wykopaliska = self.dodaj_combo("Wykopaliska",wnioski.wykopy,nazwa="wykopy")
        self.dodatkowe = self.dodaj_txt("Dane dodatkowe", wnioski.dodat, nazwa="dodat")
        
class ZagrozeniaTab(InfoTab):
    
    def __init__(self,zagr):
        InfoTab.__init__(self,1,zagr)
        self.istn_cb = self.dodaj_combo("Istnieje", zagr.istn, nazwa='istn')
        self.stal_cb = self.dodaj_combo(u"Stałe",zagr.stal,nazwa='stal')
        self.doraz_cb = self.dodaj_combo(u"Doraźne",zagr.doraz,nazwa='doraz')
        self.ludz_cb = self.dodaj_combo(u"Ludzie",zagr.ludz,nazwa='ludz')
        self.nat_cb = self.dodaj_combo(u"Natura",zagr.nat,nazwa='nat')
        self.pryw_cb = self.dodaj_combo(u"Uż. prywatny",zagr.pryw,nazwa='pryw')
        self.spol_cb = self.dodaj_combo(u"Społeczny",zagr.spol,nazwa='spol')
        self.dodaj_txt(u"Dane dodatkowe", zagr.dodat, nazwa='dodat')
                
class InfoDialog(QDialog):

    def __init__(self,dane,stan):
        QDialog.__init__(self)
        vb = QVBoxLayout()
        self.setLayout(vb)
        self.tabs = QTabWidget(self)
        vb.addWidget(self.tabs)
        self.btns = QDialogButtonBox(self)
        #self.btns.setGeometry(QtCore.QRect(70, 290, 221, 41))
        #self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.btns.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        vb.addWidget(self.btns)
        self.stan = stan
        self.dane = dane
        #self.tabs.addTab(PolozenieTab(),QApplication.translate("MainWindow", "Położenie", None,QApplication.UnicodeUTF8))
        self.poloz_tab = PolozenieTab(self.dane.polozenie(stan))
        self.tabs.addTab(self.poloz_tab,QApplication.translate("MainWindow", "Położenie", None,QApplication.UnicodeUTF8))
        self.ekspo_tab = EkspozycjaTab(self.dane.ekspozycja(stan))
        self.tabs.addTab(self.ekspo_tab,"Ekspozycja")
        self.teren_tab = TerenTab(self.dane.teren(stan))
        self.tabs.addTab(self.teren_tab,"Teren")
        self.obsz_tab = ObszarTab(self.dane.obszar(stan))
        self.tabs.addTab(self.obsz_tab,"Obszar")
        self.mater_tab = MaterialyTab(stan,self.dane)
        self.tabs.addTab(self.mater_tab,QApplication.translate("MainWindow", "Materiały", None,QApplication.UnicodeUTF8))
        self.wnioski_tab = WnioskiTab(self.dane.wnioski(stan))
        self.tabs.addTab(self.wnioski_tab,"Wnioski")
        self.zagroz_tab = ZagrozeniaTab(self.dane.zagrozenia(stan))
        self.tabs.addTab(self.zagroz_tab,QApplication.translate("MainWindow", "Zagrożenia", None,QApplication.UnicodeUTF8))
        self.setWindowTitle("Informacje")
        self.connect(self.btns,SIGNAL('rejected()'),self.anuluj)
        self.connect(self.btns,SIGNAL('accepted()'),self.zatwierdz)
        
    def anuluj(self):
        self.done(0)
        
    def zatwierdz(self):
        self.poloz_tab.zapisz()
        self.ekspo_tab.zapisz()
        self.teren_tab.zapisz()
        self.obsz_tab.zapisz()
        self.mater_tab.zapisz()
        self.wnioski_tab.zapisz()
        self.zagroz_tab.zapisz()
        self.done(0)