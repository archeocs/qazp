# -*- coding: utf-8 -*-

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialog,QVBoxLayout,QTabWidget,QDialogButtonBox,QApplication,QLineEdit
from widgety.infotab import InfoTab
from widgety.tabelatab import MaterialyTab
import uzytki

class PolozenieTab(InfoTab):
    def __init__(self,polo):
        InfoTab.__init__(self,3,polo)
        #self.jedn_txt = self.dodaj_txt("Jednostka",polo.jedn,nazwa="jedn")
        self.nadm_cb = self.dodaj_combo("Strefa nadmorska",polo.nadm,nazwa="nadm")
        self.morze_cb = self.dodaj_combo("W morzu",polo.morze,nazwa="morze")
        self.plaza_cb = self.dodaj_combo("Plaża",polo.plaza,nazwa="plaza")
        self.mierze_cb = self.dodaj_combo("Mierzeja",polo.mierz,nazwa="mierz")
        self.skarpa_cb = self.dodaj_combo("Skarpa",polo.skarpa,nazwa="skarpa")
        self.wal_cb = self.dodaj_combo("Wał wydmowy",polo.wal,nazwa="wal")
        self.sdd_cb = self.dodaj_combo("Duże doliny",polo.dd,nazwa="dd")
        self.woda_cb = self.dodaj_combo("W wodzie",polo.woda,nazwa="woda")
        self.terden_cb = self.dodaj_combo("Ter. denna",polo.terden,nazwa="terden")
        self.ternad_cb = self.dodaj_combo("Ter. nadzalewowa",polo.ternad,nazwa="ternad")
        self.terwyz_cb = self.dodaj_combo("Ter. wyższa",polo.terwyz,nazwa="terwyz")
        self.brzeg_cb = self.dodaj_combo("Brzeg wysocz.",polo.brz,nazwa="brz")
        self.smd_cb = self.dodaj_combo("Małe doliny",polo.md,nazwa="md")
        self.dnod_cb = self.dodaj_combo("Dno doliny",polo.dnod,nazwa="dnod")
        self.stokd_cb = self.dodaj_combo("Stok doliny",polo.stokd,nazwa="stokd")
        self.krawd_cb = self.dodaj_combo("Krawędź doliny",polo.krawd,nazwa="krawd")
        self.spd_cb = self.dodaj_combo("Poza dolinami",polo.pd,nazwa="pd")
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
        self.oslo_cb = self.dodaj_combo("Osłonięty",eksp.oslo,nazwa="oslo")
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
        self.niezab_cb = self.dodaj_combo("Niezabudowany",ter.niezab,nazwa="niezab")
        self.srezab_cb = self.dodaj_combo("Średniozabudowany",ter.srezab,nazwa="srezab")
        self.zab_cb = self.dodaj_combo("Zabudowany",ter.zab,nazwa="zab")
        self.las_cb = self.dodaj_combo("Las",ter.las,nazwa="las")        
        self.sad_cb = self.dodaj_combo("Sad",ter.sad,nazwa="sad")
        self.park_cb = self.dodaj_combo("Park",ter.park,nazwa="park")
        self.pole_cb = self.dodaj_combo("Pole orne",ter.orne,nazwa="orne")
        self.laka_cb = self.dodaj_combo("Łąka",ter.laka,nazwa="laka")
        self.torf_cb = self.dodaj_combo("Rolniczy prywatny",ter.pryw,nazwa="pryw")
        self.nieuz_cb = self.dodaj_combo("Rolniczy społeczny",ter.spol,nazwa="spol")        
        self.bagno_cb = self.dodaj_combo("Przemysłowy",ter.przem,nazwa="przem")
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
        #self.doraz_cb = self.dodaj_combo(u"Doraźne",zagr.doraz,nazwa='doraz')
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
        self.btns.setGeometry(70, 290, 221, 41)
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
        self.tabs.addTab(self.mater_tab,QApplication.translate("MainWindow", "Fakty kulturowe", None,QApplication.UnicodeUTF8))
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