# -*- coding: utf-8 -*-

# (c) Milosz Piglas 2013 Wszystkie prawa zastrzezone

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

from threading import Lock

TAKNIEATR = [('T', 'Tak'), ('N', 'Nie')]

RODZAJ_BADAN = [('W', 'Wykopaliska'), ('P', 'Powierzchniowe'), ('L', u'Luźne')]

class Warunek(object):
    
    def __init__(self, atrybut=None):
        self._atrs = {}
        if atrybut is not None:
            self._atrs.append(atrybut)
    
    def dodaj(self, atrybut, i):
        self._atrs[i] = atrybut
        return self
    
    @property
    def atrs(self):
        ak = self._atrs.keys()
        ak.sort()
        return [self._atrs[k] for k in ak]
        
    @property
    def tabele(self):
        return set([(a.tabela.tnazwa, a.tabela.alias) for a in self._atrs.itervalues()])
            
    def __repr__(self):
        #if len(self._atrs) == 1:
        #    return '%s = ?' % repr(self.atrs[0])
        #p = ' OR '.join(['%s = ?' % repr(a) for a in self.atrs])
        #return '( '+p+' )'
        if len(self._atrs) == 1:
            return self.atrs[0].warunek
        p = ' OR '.join([a.warunek for a in self.atrs])
        return '( '+p+' )'
        
class SqlGenerator(object):

    def __init__(self):
        self._grupy = {}
        self._warunki = {}
        self._funkcje = {}
        
    def _iterValues(self, mapa):
        sk = []
        sk.extend(mapa.iterkeys())
        sk.sort()
        for k in sk:
            yield mapa[k]
    
    @property
    def pobierane(self):
        pob = []
        pob.extend(self._iterValues(self._funkcje))
        pob.extend(self._iterValues(self._grupy))
        return pob
    
    @property
    def grupy(self):
        return self._grupy
        
    @property
    def funkcje(self):
        return self._funkcje
        
    @property
    def warunki(self):
        return self._warunki
        
    @property
    def poprawny(self):
        return len(self._grupy) > 0 and len(self._funkcje) > 0
    
    @property
    def params(self):
        pd = []
        for w in self._iterValues(self._warunki):
            pd.extend(w.atrs)
        return pd
        
    def __unicode__(self):
        tabs = set([('stanowiska', 'H')])
        seltab = set([])
        selatr = []
        for g in self._iterValues(self._grupy):
            if not isinstance(g.tabela, SelectTabela):
                tabs.add((g.tabela.tnazwa, g.tabela.alias))
            else:
                selatr.append(g)
                seltab.add(g.tabela)
            #tabs.add(repr(g.tabela))
        for t in seltab:
            tatr = [a for a in selatr if a.tabela == t]
            tabs.add((t.select(tatr), t.alias))
        for a in self._iterValues(self._warunki):
            tabs = tabs.union(a.tabele)
        if len(self._grupy) == 0 or len(self._funkcje) == 0:
            raise Exception('Nie zdefiniowano grupowania')
        gbp = ','.join([repr(atr) for atr in self._iterValues(self._grupy)])
        wh = ' AND '.join([repr(w) for w in self._iterValues(self._warunki)])
        if wh.strip() != '':
            wh = 'WHERE ' + wh
        jo = 'stanowiska H'
        for t in tabs:
            if t[0] != 'stanowiska':
                jo += ' join %s on %s.stanowisko = H.id ' % (t[0]+' '+t[1], t[1])
        fun = ', '.join([repr(atr) for atr in self._iterValues(self._funkcje)])
        return 'SELECT %s, %s FROM %s %s GROUP BY %s' % (fun, gbp, jo, wh, gbp)


class Atrybut(object):

    def __init__(self, nazwa, dozwolone=None, etykieta=None): 
        # jezeli dowolone == None to znaczy ze kazda wartosc jest dozwolona
        self._nazwa = nazwa
        self._dozwolone = dozwolone
        self._etykieta = etykieta
        self._tabela = None
    
    def _initDozwolone(self):
        pass
    
    @property    
    def anazwa(self):
        return self._nazwa
    
    @property
    def dozwolone(self): # zwraca etykiety dozwolonych wartosci
        self._initDozwolone()
        if self._dozwolone is not None:
            return [d[1] for d in self._dozwolone]
        return None
    
    @property
    def dowolnaWartosc(self):
        self._initDozwolone()
        return self._dozwolone is None
    
    def dodajKod(self, symbol, etykieta):
        self._initDozwolone()
        if self._dozwolone is None:
            self._dozwolone = []
        self._dozwolone.append((symbol, etykieta))
        return self
    
    def kodwar(self, i):
        self._initDozwolone()
        return self._dozwolone[i][0]
    
    def etwar(self, i):
        self._initDozwolone()
        return self._dozwolone[i][1]

    @property    
    def aetykieta(self):
        return self._etykieta

    def setTabela(self, t):
        self._tabela = t
        
    def getTabela(self):
        return self._tabela
        
    tabela = property(getTabela, setTabela)

    def __unicode__(self):
        return self._etykieta

    def __repr__(self):
        if self._tabela is None:
            return self._nazwa
        return self._tabela.alias+'.'+self._nazwa
    
    def toStr(self):
        if self._tabela is None:
            return self._etykieta
        return self._tabela.tetykieta+'.'+self._etykieta
    
    def odtworz(self, kod):
        self._initDozwolone()
        for d in self._dozwolone:
            if d[0] == kod:
                return d[1]
        return ''

    @property    
    def warunek(self):
        return repr(self)+' = ?'

class DynAtrybut(Atrybut):

    def __init__(self, nazwa, select, etykieta, con): 
        # polecenie select w pierwszych dwoch kolumnach musi zwracac pare (kod, wartosc)
        Atrybut.__init__(self, nazwa, etykieta=etykieta)
        self._prepDoz = con.prep(select)
        self._lock = Lock()
        
    def _initDozwolone(self):
        self._lock.acquire()
        if self._dozwolone is None:
            self._dozwolone = []
            for p in self._prepDoz.wszystkie():
                self._dozwolone.append((p[0], p[1]))
        self._lock.release() 

class FaktyAtrybut(DynAtrybut):

    def __init__(self, con, nazwa, etykieta, tabela, wherePola):
        DynAtrybut.__init__(self, nazwa, 'select kod, skrot from '+tabela+' order by skrot', 
                                    etykieta, con)
        self._wherePola = wherePola
        
    def odtworz(self, wartosc): 
        #return wartosc
        tw = wartosc.split('#') # jeda, jedb, rel, pewnosc
        self._initDozwolone()
        for d in self._dozwolone:
            if d[0] == tw[0]:
                r = d[1]
                break
        if tw[1] != '':
            for d in self._dozwolone:
                if d[0] == tw[1] and tw[2] == 'Z':
                    r += '-'+d[1]
                    break
                elif d[0] == tw[1] and tw[2] == 'P':
                    r += '/'+d[1]
        if tw[3] != '' and float(tw[3]) < 1:
            r = '?'+r
        return r

    @property
    def warunek(self):
        return '? in ( %s )' % (','.join([self.tabela.alias+'.'+wp 
                                            for wp in self._wherePola]))
                                            
    
def atrsTab(tab):
    atrs = []
    for t in tab:
        atrs.append(Atrybut(t[0], t[1], t[2]))
    return atrs


class Tabela(object):
    
    def __init__(self, nazwa, atrybuty, etykieta, alias):
        self._nazwa = nazwa
        self._atrs = atrybuty
        self._etykieta = etykieta
        self._alias = alias
        for a in self._atrs:
            a.tabela = self
    
    def __getitem__(self, indeks):
        return self._atrs[indeks]
    
    @property    
    def tnazwa(self):
        return self._nazwa
    
    @property
    def atrs(self):
        return self._atrs

    @property
    def tetykieta(self):
        return self._etykieta
    
    @property
    def alias(self):
        return self._alias
    
    def dodajAtr(self, nazwa, etykieta, dozwolone=None):
        a = Atrybut(nazwa, etykieta=etykieta, dozwolone=dozwolone)
        self._atrs.append(a)
        a.tabela = self
        return a
    
    def dodajAtrybut(self, atrybut):
        self._atrs.append(atrybut)
        atrybut.tabela = self

    def _nowyFiltr(self, atrs):
        """
        Tworzy polecenie sql do wyszukania stanowisk spelniajacyh okreslone 
        kryteria oraz przygotowuje wartosci parametrow

        atrs - atrybuty w wybranej tabeli na podstawie ktorych maja byc wyszukane 
        stanowiska. 

        return para (polecenie sql, lista wartosci parametrow)
        """
        sql = u'select distinct stanowisko from %s where '%self._nazwa
        params = []
        c = 0
        for a, v in atrs.iteritems():
            if len(v) > 1:
                war = '%s in (%s) ' % (a.anazwa, ','.join(['?' for x in range(len(v))]))
                for y in v:
                    params.append(unicode(y))
            else:
                war = '%s = ? '% a.anazwa
                params.append(unicode(v[0]))
            if c > 0:
                sql += ' and '
            sql += war
            c += 1
        sql += 'order by stanowisko'
        return (sql, params)

    def filtr(self, atrs):
        return self._nowyFiltr(atrs)
        
    def __unicode__(self):
        return self._etykieta
        
    def __repr__(self):
        return self._nazwa

class SelectTabela(Tabela):

    def __init__(self, nazwa, etykieta, alias, mapaAtr, notnull=True, genfiltr=None):
        Tabela.__init__(self, nazwa, [], etykieta, alias)
        self._matr = mapaAtr
        self._notnull = notnull
        self._genfiltr = genfiltr
        
    def select(self, atrs):
        sql = '(select distinct stanowisko, %s from '+self.tnazwa+' %s )'
        kols = ', '.join(['%s as %s' % (self._matr[a.anazwa], a.anazwa) for a in atrs])
        if self._notnull:
            warunek = ' OR '.join(['%s is not null' % a.anazwa for a in atrs])
            return sql % (kols, ' WHERE '+warunek) 
        return sql % kols 

    def filtr(self, atrs):
        if self._genfiltr is None:
            return Tabela._nowyFiltr(self, atrs)
        return self._genfiltr(atrs)

def fizgeo():
    t = Tabela('fizgeo_dane', [], 'Jed. fiz.-geo.', 'A')
    t.dodajAtr('nadmorska', u'Nadmorska', TAKNIEATR)
    t.dodajAtr('w_morzu', u'W morzu', TAKNIEATR)
    t.dodajAtr('plaza', u'Plaża', TAKNIEATR)
    t.dodajAtr('mierzeja', u'Mierzeja', TAKNIEATR)
    t.dodajAtr('skarpa', u'Skarpa', TAKNIEATR)
    t.dodajAtr('wal_wydmowy', u'Wał wydmowy', TAKNIEATR)
    t.dodajAtr('duze_doliny', u'Duże doliny', TAKNIEATR)
    t.dodajAtr('w_wodzie', u'W wodzie', TAKNIEATR)
    t.dodajAtr('ter_denna', u'Ter. denna', TAKNIEATR)
    t.dodajAtr('ter_nadzalewowa', u'Ter. nadzalewowa', TAKNIEATR)
    t.dodajAtr('ter_wyzsze', u'Ter. wyższe', TAKNIEATR)
    t.dodajAtr('brzeg_wysoczyzny', u'Brzeg wysoczyzny', TAKNIEATR)
    t.dodajAtr('male_doliny', u'Małe doliny', TAKNIEATR)
    t.dodajAtr('dno_doliny', u'Dno doliny', TAKNIEATR)
    t.dodajAtr('stok_doliny', u'Stok doliny', TAKNIEATR)
    t.dodajAtr('krawedz_doliny', u'Krawędź doliny', TAKNIEATR)
    t.dodajAtr('poza_dolinami', u'Poza dolinami', TAKNIEATR)
    t.dodajAtr('rownina', u'Równina', TAKNIEATR)
    t.dodajAtr('obsz_falisty', u'Obsz. falisty', TAKNIEATR)
    t.dodajAtr('obsz_pagorkowaty', u'Obsz. pagórkowaty', TAKNIEATR)
    t.dodajAtr('obsz_gorzysty', u'Obsz. górzysty', TAKNIEATR)
    return t

def obszar():
    t = Tabela('obszar_dane', [], 'Obszar', 'B')
    t.dodajAtr('obserwacja', u'Obserwacja')\
        .dodajKod('U', u'Utrudniona')\
        .dodajKod('B', u'Bez przeszkód')
    t.dodajAtr('pole', 'Pole')\
        .dodajKod('O', 'Otwarte')\
        .dodajKod('Z', u'Zamknięte')
    t.dodajAtr('nasyc_rozklad', u'Rozkład nasycenia')\
        .dodajKod('R', u'Równomierny')\
        .dodajKod('N', u'Nierównomierny')
    t.dodajAtr('nasyc_typ', u'Typ nasycenia')\
        .dodajKod('J', u'Jednocentryczny')\
        .dodajKod('W', u'Wielocentryczne')\
        .dodajKod('D', u'Dekocentryczne')
    t.dodajAtr('gestosc_znal', u'Gęstość znalezisk')\
        .dodajKod('M', u'Mała')\
        .dodajKod('S', u'Średnia')\
        .dodajKod('D', u'Duża')
    return t

def teren():
    t = Tabela('teren_dane', [], 'Teren', 'C')
    t.dodajAtr('zabudowany', u'Zabudowany', TAKNIEATR)
    t.dodajAtr('sred_zabud', u'Śred. zabudowany', TAKNIEATR)
    t.dodajAtr('prywatny', u'Prywatny', TAKNIEATR)
    t.dodajAtr('spoleczny', u'Społeczny', TAKNIEATR)
    t.dodajAtr('przemyslowy', u'Przemysłowy', TAKNIEATR)
    t.dodajAtr('nieuzytek', u'Nieużytek', TAKNIEATR)
    t.dodajAtr('las', u'Las', TAKNIEATR)
    t.dodajAtr('sad', u'Sad', TAKNIEATR)
    t.dodajAtr('park', u'Park', TAKNIEATR)
    t.dodajAtr('pole_orne', u'Pole orne', TAKNIEATR)
    t.dodajAtr('laka', u'Łąka', TAKNIEATR)
    t.dodajAtr('torf', u'Torf', TAKNIEATR)
    t.dodajAtr('woda', u'Woda', TAKNIEATR)
    t.dodajAtr('bagno', u'Bagno', TAKNIEATR)
    return t

def gleba():
    t = Tabela('gleba_dane', [], 'Gleba', 'D')
    t.dodajAtr('luzna', u'Luźna', TAKNIEATR)
    t.dodajAtr('zwiezla', u'Zwięzła', TAKNIEATR)
    t.dodajAtr('torf_bag', u'Torf.-bag', TAKNIEATR)
    t.dodajAtr('kamienistosc', u'Kamienistość')\
        .dodajKod('M', u'Mała')\
        .dodajKod('S', u'Średnia')\
        .dodajKod('D', u'Duża')
    return t
    
def wnioski():
    t = Tabela('wnioski', [], 'Wnioski', 'E')
    t.dodajAtr('wartosc', u'Wartość')\
        .dodajKod('M', u'Mała')\
        .dodajKod('S', u'Średnia')\
        .dodajKod('D', u'Duża')
    t.dodajAtr('inwentaryzacja', u'Inwentaryzacja', TAKNIEATR)
    t.dodajAtr('interwencja', u'Interwencja', TAKNIEATR)
    t.dodajAtr('wykopaliska', u'Wykopaliska', TAKNIEATR)
    return t
        
def ekspozycja():
    t = Tabela('ekspozycja_dane', [], 'Ekspozycja', 'F')
    t.dodajAtr('eksponowany', u'Eksponowany', TAKNIEATR)
    t.dodajAtr('kraw_stoki', u'Krawędzie, stoki', TAKNIEATR)
    t.dodajAtr('sfaldowania_cyple', u'Sfałdowania, cyple', TAKNIEATR)
    t.dodajAtr('cyple_wybitne', u'Cyple wybitne', TAKNIEATR)
    t.dodajAtr('waly_garby', u'Wały, garby', TAKNIEATR)
    t.dodajAtr('wyniesienia_okrezne', u'Wyniesienia okrężne', TAKNIEATR)
    t.dodajAtr('osloniety', u'Osłonięty', TAKNIEATR)
    t.dodajAtr('podst_stoku', u'Podstawa stoku', TAKNIEATR)
    t.dodajAtr('doliny_niecki', u'Doliny, niecki', TAKNIEATR)
    t.dodajAtr('kotlinki_zagleb', u'Kotlinki, zagłębienia', TAKNIEATR)
    t.dodajAtr('jaskinie', u'Jaskinie', TAKNIEATR)
    t.dodajAtr('stopien', u'Stopień')
    t.dodajAtr('rozmiar', u'Rozmiar')
    t.dodajAtr('kierunek', u'Kierunek')
    return t

def zagrozenia():
    t = Tabela('zagrozenia', [], u'Zagrożenia', 'G')
    t.dodajAtr('wystepowanie', u'Występowanie')\
        .dodajKod('I', 'Istnieje')\
        .dodajKod('N', 'Nie istnieje')
    t.dodajAtr('czas', 'Czas')\
        .dodajKod('S', u'Stałe')\
        .dodajKod('D', u'Doraźne')
    t.dodajAtr('przyczyna_ludzie', u'Przyczyna:Ludzie', TAKNIEATR)
    t.dodajAtr('przyczyna_natura', u'Przyczyna:Natura', TAKNIEATR)
    t.dodajAtr('uzytkownik_spoleczny', u'Użytkownik pryw.', TAKNIEATR)
    t.dodajAtr('uzytkownik_prywatny', u'Użytkownik społ.', TAKNIEATR)
    return t

def stanowiska(con):
    t = Tabela('stanowiska', [], u'Stanowiska', 'H')
    t.dodajAtr('obszar', u'Obszar AZP')
    t.dodajAtr('nr_obszar', u'Numer AZP')
    t.dodajAtrybut(DynAtrybut('miejscowosc', 'select id, nazwa from miejscowosci order by nazwa', u'Miejscowość', con))
    t.dodajAtr('nr_miejscowsc', u'Numer w miejscowości')
    t.dodajAtrybut(DynAtrybut('gmina', 'select id, nazwa from gminy order by nazwa', u'Gmina', con))
    t.dodajAtr('rodzaj_badan', u'Rodzaj badań', RODZAJ_BADAN)
    return t
    
def klasyfikacja(con):
    t = Tabela('fakty', [], 'Fakty', 'J')
    t.dodajAtrybut(DynAtrybut('okresa', 'select kod, skrot from okresy_dziejow order by skrot', 'OkresA', con))
    t.dodajAtrybut(DynAtrybut('okresb', 'select kod, skrot from okresy_dziejow order by skrot', 'OkresB', con))
    t.dodajAtr('okr_relacja', 'OkresRelacja').dodajKod('Z', '-').dodajKod('P', '/')
    t.dodajAtr('okr_pewnosc', u'OkresPewność')
    t.dodajAtrybut(DynAtrybut('jeda', 'select kod, skrot from jednostki order by skrot', 'JednostkaA', con))
    t.dodajAtrybut(DynAtrybut('jedb', 'select kod, skrot from jednostki order by skrot', 'JednostkaB', con))
    t.dodajAtr('jed_relacja', 'JednostkaRelacja').dodajKod('Z', '-').dodajKod('P', '/')
    t.dodajAtr('jed_pewnosc', u'JednostkaPewność')
    t.dodajAtrybut(DynAtrybut('funkcja', 'select kod, skrot from funkcje order by skrot', 'Funkcja', con))
    t.dodajAtr('fun_pewnosc', u'FunkcjaPewność')
    t.dodajAtr('masowy', 'M. masowy')
    t.dodajAtr('wydzielony', 'M. wydzielony')
    return t


def _faktyFiltr(atrs):
    sql = u'select distinct stanowisko from fakty where '
    params = {}
    c, pc = 0, 0
    for a, v in atrs.iteritems():
        if a.anazwa == 'jednostka':
            rpola = ['jeda', 'jedb']
        elif a.anazwa == 'okres':
            rpola = ['okresa', 'okresb']
        else:
            rpola = ['funkcja']
        if len(v) > 1:
            #parstr = ','.join([':p'+str(pc+x) for x in range(len(v))])
            tpar = []
            for (yi, y) in enumerate(v):
                tpar.append(':p'+str(pc+yi))
                params['p'+str(pc+yi)] = unicode(y)
            pc += len(v)
            parstr = ','.join(tpar)
            if len(rpola) == 2:
                war = '%s in (%s) OR %s in (%s) ' % (rpola[0], parstr, rpola[1], parstr)
            else:
                war = '%s in (%s) ' % (rpola[0], parstr)
        else:
            if len(rpola) == 2:
                war = '%s = :p%d OR %s = :p%d ' % (rpola[0], pc, rpola[1], pc)
            else:
                war = '%s = :p%d ' % (rpola[0], pc)
            params['p'+str(pc)] = unicode(v[0])
            pc += 1
        if c > 0:
            sql += ' AND '
        sql += war
        c += 1
    sql += 'order by stanowisko'
    return (sql, params)
    
def fakty(con):
    mapa = {'jednostka' : "jeda||'#'||coalesce(jedb,'')||'#'||coalesce(jed_relacja,'')||'#'||coalesce(jed_pewnosc,'')",
            'okres' : "okresa||'#'||coalesce(okresb,'')||'#'||coalesce(okr_relacja,'')||'#'||coalesce(okr_pewnosc,'')",
            'fun': "funkcja||'###'||coalesce(fun_pewnosc,'')"
    }
    t = SelectTabela('fakty', u'Fakty', 'J', mapa, genfiltr=_faktyFiltr)
    t.dodajAtrybut(FaktyAtrybut(con, 'jednostka', 'Jednostka', 'jednostki', ['jeda', 'jedb']))
    t.dodajAtrybut(FaktyAtrybut(con, 'okres', 'Okres', 'okresy_dziejow', ['okresa', 'okresb']))
    t.dodajAtrybut(FaktyAtrybut(con, 'fun', 'Funkcja', 'funkcje', ['funkcja']))
    return t
    
WSZYSTKIE = [zagrozenia(), ekspozycja(), wnioski(), gleba(), teren(), obszar(), fizgeo()]
