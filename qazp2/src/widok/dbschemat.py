# -*- coding: utf-8 -*-

from .qtqube.pyqube.views import View, ViewAttr, Schema, AttrPair, Relation
from .qtqube.pyqube import *
from collections import namedtuple
from functools import partial

Atr = namedtuple('Atr', ['nazwa', 'opis'])
para = namedtuple('para', ['atra', 'atrb'])

def utworzWidok(tabela, nazwa, atrybuty):
    widok = View(tabela, nazwa, [])
    for a in atrybuty:
        widok.attrs[a.nazwa] = ViewAttr(a.nazwa, widok, a.opis)
    return widok
    
def utworzRelacje(awidok, bwidok, pary):
    atrPary = []
    for p in pary:
        atrPary.append(AttrPair(awidok.attribute(p.atra), 
                                bwidok.attribute(p.atrb)
                                )
                      )
    return Relation(atrPary)

def stanowiska():
    atrybuty = [
        Atr('id', 'Id'),
        Atr('obszar', 'Obszar AZP'),
        Atr('nr_obszar', 'Numer AZP'),
        Atr('miejscowosc', u'Miejscowość'),
        Atr('nr_miejscowosc', u'Numer w miejscowości'),
        Atr('gmina', 'Gmina'),
        Atr('powiat', 'Powiat'),
        Atr('wojewodztwo', u'Województwo'),
        Atr('rodzaj_badan', u'Rodzaj badań'),
        Atr('data', u'Data badań'),
        Atr('autor', u'Autor'),
        Atr('uwagi', u'Uwagi') ]
    return utworzWidok('stanowiska', 'Stanowisko', atrybuty)

def ekspozycja():
    atrybuty = [
        Atr('id', 'Id'),
        Atr('stanowisko', 'Stanowisko'),
        Atr('eskponowany', 'Teren eksponowany'),
        Atr('kraw_stoki', u'Krawędź, stok'),
        Atr('sfaldowania_cyple', u'Sfałdowanie, cypel'),
        Atr('waly_garby', u'Wały, garby'),
        Atr('wyniesienia_okrezne', u'Wyniesienia okrężne'),
        Atr('osloniety', u'Teren osłonięty'),
        Atr('podst_stoku', u'Podstawa stoku'),
        Atr('doliny_niecki', u'Doliny, niecki'),
        Atr('kotlinki_zagleb', u'Kotlinki, zagłębienia'),
        Atr('jaskinie', u'Jaskinie'),
        Atr('rozmiar', u'Rozmiar'),
        Atr('stopien', u'Stopień'),
        Atr('kierunek', u'Kierunek'),
        Atr('uwagi', u'Uwagi')]
    return utworzWidok('ekspozycja_dane', 'Ekspozycja', atrybuty)

def polozenie():
    atrybuty = [
        Atr('id', 'Id'),
        Atr('stanowisko', 'Stanowisko'),
        Atr('nadmorska', 'Strefa nadmorska'),
        Atr('w_morzu', 'W morzu'),
        Atr('plaza', u'Plaża'),
        Atr('mierzeja', u'Mierzeja'),
        Atr('skarpa', 'Skarpa'),
        Atr('wal_wydmowy', u'Wał wydmowy'),
        Atr('duze_doliny', u'Duże doliny'),
        Atr('w_wodzie', 'W wodzie'),
        Atr('ter_denna', 'Terasa denna'),
        Atr('ter_nadzalewowa', 'Terasa nadzalewowa'),
        Atr('ter_wyzsze', u'Terasy wyższe'),
        Atr('brzeg_wysoczyzny', 'Brzeg wysoczyzny'),
        Atr('male_doliny', u'Małe doliny'),
        Atr('dno_doliny', 'Dno doliny'),
        Atr('stok_doliny', 'Stok doliny'),
        Atr('krawedz_doliny', u'Krawędź doliny'),
        Atr('poza dolinami', 'Strefa poza dolinami'),
        Atr('rownina', u'Równina'),
        Atr('obsz_falisty', u'Obszar falisty'),
        Atr('obsz_pagorkowaty', u'Obszar pagórkowaty'),
        Atr('obsz_gorzysty', u'Obszar górzysty'),
        Atr('uwagi', u'Uwagi')]
    return utworzWidok('fizgeo_dane', u'Położenie', atrybuty)

def obszar():
    atrybuty = [
        Atr('id', 'Id'),
        Atr('stanowisko', 'Stanowisko'),
        Atr('obserwacja', 'Obserwacja'),
        Atr('pole', 'Pole'),
        Atr('nasycenie_rozklad', u'Rozkład nasycenia'),
        Atr('nasycenie_typ', u'Typ nasycenia'),
        Atr('powierzchnia', u'Powierzchnia'),
        Atr('gestosc_znal', u'Gęstość znalezisk'),
        Atr('uwagi', u'Uwagi')]
    return utworzWidok('obszar_dane', 'Obszar', atrybuty)
     
def teren():
    atrybuty = [
        Atr('id', 'Id'),
        Atr('stanowisko', 'Stanowisko'),
        Atr('zabudowany', 'Zabudowany'),
        Atr('sred_zabud', u'Średnio zabudowany'),
        Atr('las', 'Las'),
        Atr('sad', 'Sad'),
        Atr('park', 'Park'),
        Atr('pole_orne', 'Pole orne'),
        Atr('laka', u'Łąka'),
        Atr('nieuzytek', u'Nieużytek'),
        Atr('torf', 'Torf'),
        Atr('woda', 'Woda'),
        Atr('bagno', 'Bagno'),
        Atr('prywatny', 'Prywatny'),
        Atr('spoleczny', u'Społeczny'),
        Atr('przemyslowy', u'Przemysłowy'),
        Atr('uwagi', 'Uwagi')]
    return utworzWidok('teren_dane', 'Teren', atrybuty)

def wnioski():
    atrybuty = [
        Atr('id', 'Id'),
        Atr('stanowisko', 'Stanowisko'),
        Atr('wartosc', u'Wartość poznawcza'),
        Atr('inwentaryzacja', u'Inwentaryzacja'),
        Atr('wykopaliska', 'Wykopaliska'),
        Atr('interwencja', 'Interwencja administracyjna'),
        Atr('uwagi', 'Uwagi')]
    return utworzWidok('wnioski', 'Wnioski', atrybuty)
    
def zagrozenia():
    atrybuty = [
        Atr('id', 'Id'),
        Atr('stanowisko', 'Stanowisko'),
        Atr('wystepowanie', u'Występowanie'),
        Atr( 'czas', 'Czas'),
        Atr( 'przyczyna_ludzie', u'Ludzie'),
        Atr( 'przyczyna_natura', u'Natura'),
        Atr( 'uzytkownik_spoleczny', u'Użytkownik społeczny'),
        Atr( 'uzytkownik_prywatny', u'Użytkownik prywatny'),
        Atr( 'uwagi', u'Uwagi')]
    return utworzWidok('zagrozenia', u'Zagrożenia', atrybuty)    

def aktualnosci():
    atrybuty = [
        Atr('id', 'Id'),
        Atr('stanowisko', 'Stanowisko'),
        Atr('magazyn', 'Magazyn'),
        Atr('nr_inwentarza', 'Nr inwentarza'),
        Atr('nr_krz', u'Nr rejestru zabytków'),
        Atr('data_krz', u'Data rejestru zabytków'),
        Atr('park', u'Park kulturowy'),
        Atr('plan', u'Plan zagospodarowania przestrzennego'),
        Atr('wlasciciel', u'Właściciel'),
        Atr('uwagi', u'Uwagi')]
    return utworzWidok('aktualnosci', u'Aktualności', atrybuty)
    
def fakty():
    atrybuty = [
        Atr('id', 'Id'),
        Atr('stanowisko', 'Stanowisko'),
        Atr('okresa', 'Okres A'),
        Atr('okresb', 'Okres B'),
        Atr('okr_relacja', 'Okresy - relacja'),
        Atr('okr_pewnosc', u'Okresy - pewność'),
        Atr('jeda', 'Jednostka kulturowa A'),
        Atr('jedb', 'Jednostka kulturowa B'),
        Atr('jed_relacja', 'Jednostki - relacja'),
        Atr('jed_pewnosc', u'Jednostki - pewnosć'),
        Atr('funkcja', u'Funkcja obiektu'),
        Atr('fun_pewnosc', u'Funkcja - pewność'),
        Atr('masowy', u'Materiały masowe'),
        Atr('wydzielony', u'Materiały wydzielone')]
    return utworzWidok('fakty', 'Fakty', atrybuty)

def gleba():
    atrybuty = [
        Atr('id', 'Id'),
        Atr('stanowisko', 'Stanowisko'),
        Atr('luzna', u'Luźna'),
        Atr('zwiezla', u'Zwięzła'),
        Atr('torf_bag', u'Torfowo-bagnista'),
        Atr('kamienistosc', u'Kamienistość'),
        Atr('uwagi', 'Uwagi')]
    return utworzWidok('gleba_dane', 'Gleba', atrybuty)
    
def karta():
    atrybuty = [
        Atr('id', 'Id'),
        Atr('stanowisko', 'Stanowisko'),
        Atr('nazwa_lok', 'Nazwa lokalna'),
        Atr('arkusz_mapy', 'Arkusz mapy'),
        Atr('dalsze_losy', 'Dalsze losy'),
        Atr('dzieje_badan', u'Dzieje badań'),
        Atr('metryka_hist', 'Metryka historyczna'),
        Atr('literatura', 'Literatura'),
        Atr('dzialka_geodezyjna', u'Działka geodezyjna'),
        Atr('egb', 'egb'),
        Atr('autorzy', 'Autorzy'),
        Atr('chronologia', u'Określił chronologię'),
        Atr('konsultant', u'Konsultant AZP'),
        Atr('uwagi', 'Uwagi')]
    return utworzWidok('karty', 'Karta', atrybuty)

def okresb():
    atrybuty = [
        Atr('kod', 'Kod'),
        Atr('epoka', 'Epoka'),
        Atr('okres', 'Okres'),
        Atr('nazwa', 'Nazwa')]
    return utworzWidok('okresy_dziejow', 'OkresB', atrybuty)
    
def okresa():
    atrybuty = [
        Atr('kod', 'Kod'),
        Atr('epoka', 'Epoka'),
        Atr('okres', 'Okres'),
        Atr('nazwa', 'Nazwa')]
    return utworzWidok('okresy_dziejow', 'OkresA', atrybuty)
    
def jednostkaa():
    atrybuty = [
        Atr('kod', 'Kod'),
        Atr('okres','Okres-kod'),
        Atr('czlon1', u'Kultura'),
        Atr('czlon2', u'Faza'),
        Atr('nazwa', u'Jednostka')]
    return utworzWidok('jednostki', 'JednostkaA', atrybuty)
     
def jednostkab():
    atrybuty = [
        Atr('kod', 'Kod'),
        Atr('okres','Okres-kod'),
        Atr('czlon1', u'Kultura'),
        Atr('czlon2', u'Faza'),
        Atr('nazwa', u'Jednostka')]
    return utworzWidok('jednostki', 'JednostkaB', atrybuty)
     
def funkcja():
    atrybuty = [
        Atr('kod', 'Kod'),
        Atr('funkcja', 'Zakres'),
        Atr('czlon1', u'Szczegół-1'),
        Atr('czlon2', u'Sczegół-2'),
        Atr('czlon3', u'Szczegół-3'),
        Atr('nazwa', u'Funkcja')]
    return utworzWidok('funkcje', 'Fukcja', atrybuty)
        

def lokalizacja(tabela, nazwa):
    atrybuty = [
        Atr('id', 'Id'),
        Atr('nazwa', 'Nazwa') ]
    return utworzWidok(tabela, nazwa, atrybuty) 
    
def relacjaStanowisko(stanowiskoWidok, widok):
    pary = [
        para('id', 'stanowisko')
    ]
    return utworzRelacje(stanowiskoWidok, widok, pary)

def relacjaFakty(faktyWidok, atr, widok):
    pary = [
        para(atr, 'kod')
    ]
    return utworzRelacje(faktyWidok, widok, pary)

def dodajWszystkie(builder, schemat, nazwa):
    widok = schemat.viewByName(nazwa)
    for v in widok.attrs.values():
        builder.select(v.select())

def utworzSchemat():
    schemat = Schema()
    stanowiskaWidok = stanowiska()
    schemat.addView(stanowiskaWidok)
    
    miejscowosciWidok = lokalizacja('miejscowosci', u'Miejscowość')
    gminyWidok = lokalizacja('gminy', u'Gmina')
    powiatWidok = lokalizacja('powiaty', u'Powiat')
    wojewodztwoWidok = lokalizacja('wojewodztwa', u'Województwa')
    
    relStanMiej = utworzRelacje(stanowiskaWidok, miejscowosciWidok,
                                [para('miejscowosc', 'id')])
    schemat.addView(miejscowosciWidok, relStanMiej)
    
    relStanGm = utworzRelacje(stanowiskaWidok, gminyWidok,
                                [para('gmina', 'id')])
    schemat.addView(gminyWidok, relStanGm)
    
    relStanPow = utworzRelacje(stanowiskaWidok, powiatWidok,
                                [para('powiat', 'id')])
    schemat.addView(powiatWidok, relStanPow)
    
    relStanWoj = utworzRelacje(stanowiskaWidok, wojewodztwoWidok,
                                [para('wojewodztwo', 'id')])
    schemat.addView(wojewodztwoWidok, relStanWoj)
    
    funRelSt = partial(relacjaStanowisko, stanowiskaWidok)
    
    ekspozycjaWidok = ekspozycja()
    schemat.addView(ekspozycjaWidok, funRelSt(ekspozycjaWidok))
    
    polozenieWidok = polozenie()
    schemat.addView(polozenieWidok, funRelSt(polozenieWidok))
    
    terenWidok = teren()
    schemat.addView(terenWidok, funRelSt(terenWidok))
    
    obszarWidok = obszar()
    schemat.addView(obszarWidok, funRelSt(obszarWidok))
    
    wnioskiWidok = wnioski()
    schemat.addView(wnioskiWidok, funRelSt(wnioskiWidok))
    
    zagrozeniaWidok = zagrozenia()
    schemat.addView(zagrozeniaWidok, funRelSt(zagrozeniaWidok))
    
    aktualnosciWidok = aktualnosci()
    schemat.addView(aktualnosciWidok, funRelSt(aktualnosciWidok))
    
    glebaWidok = gleba()
    schemat.addView(glebaWidok, funRelSt(glebaWidok))
    
    kartaWidok = karta()
    schemat.addView(kartaWidok, funRelSt(kartaWidok))
    
    faktyWidok = fakty()
    schemat.addView(faktyWidok, funRelSt(faktyWidok))
    
    okresWidokA = okresa()
    schemat.addView(okresWidokA, relacjaFakty(faktyWidok, 'okresa', okresWidokA))
    okresWidokB = okresb()
    schemat.addView(okresWidokB, relacjaFakty(faktyWidok, 'okresb', okresWidokB))
    
    jednostkaWidokA = jednostkaa()
    schemat.addView(jednostkaWidokA, relacjaFakty(faktyWidok, 'jeda', jednostkaWidokA))
    jednostkaWidokB = jednostkab()
    schemat.addView(jednostkaWidokB, relacjaFakty(faktyWidok, 'jedb', jednostkaWidokB))
    
    funkcjaWidok = funkcja()
    schemat.addView(funkcjaWidok, relacjaFakty(faktyWidok, 'funkcja', funkcjaWidok))
    return schemat
