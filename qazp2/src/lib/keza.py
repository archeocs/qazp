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

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from lib.media import odczyt
from lib.fkwykazy import WykazFaktow, funWykaz, jedWykaz, okrWykaz
from os.path import abspath

KOLEJNOSC = ['obszar', 'nr_obszar', 'miej', 'nr_miejscowosc', 'gm', 
             'pow', 'woj', 'rodzaj_badan', 'data', 'autor', 'uwagi', 
             'nadmorska', 'w_morzu', 'plaza', 'mierzeja', 'skarpa', 
             'wal_wydmowy', 'duze_doliny', 'w_wodzie', 'ter_denna', 
             'ter_nadzalewowa', 'ter_wyzsze', 'brzeg_wysoczyzny', 
             'male_doliny', 'dno_doliny', 'stok_doliny', 'krawedz_doliny', 
             'poza_dolinami', 'rownina', 'obsz_falisty', 'obsz_pagorkowaty',
              'obsz_gorzysty', 'fuwagi', 'obserwacja', 'pole', 'nasyc_rozklad',
            'nasyc_typ', 'powierzchnia', 'gestosc_znal', 'ouwagi', 
               'zabudowany', 'sred_zabud', 'las', 'sad', 'park', 
               'pole_orne', 'laka', 'nieuzytek','woda','torf','bagno', 
               'prywatny', 'spoleczny', 'przemyslowy', 'tuwagi', 'wartosc',
                'inwentaryzacja', 'wykopaliska', 'interwencja', 'wuwagi', 
                'wystepowanie', 'przyczyna_ludzie', 'przyczyna_natura', 
                'uzytkownik_spoleczny', 'uzytkownik_prywatny', 'czas','zuwagi', 
                'eksponowany', 'kraw_stoki', 'sfaldowania_cyple', 
                'cyple_wybitne', 'waly_garby', 'wyniesienia_okrezne', 
                'osloniety', 'podst_stoku', 'doliny_niecki', 
                'kotlinki_zagleb', 'jaskinie', 'rozmiar', 'stopien', 
                'kierunek', 'euwagi', 'luzna', 'zwiezla', 'ug_torfbag', 
                'specjalistyczne','kamienistosc', 'nr_krz', 'data_krz', 
                'park_kult', 'plan_zp', 'magazyn', 'nr_inwentarza', 
                'nazwa_lok', 'dalsze_losy', 'historia','metryka_hist', 
                'literatura', 'dzialka_geodezyjna', 'egb', 'chronologia', 
                'konsultant', 'kuwagi','stanowisko']

def mkmapa(t):
    return dict(zip(KOLEJNOSC,t))

def prepSt(con):
    sql = '''
    select 
    s.obszar, s.nr_obszar,m.nazwa as miej,nr_miejscowosc,g.nazwa as gm,p.nazwa as pow,ww.nazwa as woj,s.rodzaj_badan,s.data,s.autor,s.uwagi,
    f.nadmorska, f.w_morzu, f.plaza, f.mierzeja, f.skarpa, f.wal_wydmowy, f.duze_doliny, f.w_wodzie,
    f.ter_denna, f.ter_nadzalewowa, f.ter_wyzsze, f.brzeg_wysoczyzny, 
    f.male_doliny, f.dno_doliny, f.stok_doliny, f.krawedz_doliny, f.poza_dolinami, f.rownina,
    f.obsz_falisty, f.obsz_pagorkowaty, f.obsz_gorzysty, f.uwagi as fuwagi,
    o.obserwacja, o.pole, o.nasyc_rozklad, o.nasyc_typ, o.powierzchnia, o.gestosc_znal, o.uwagi as ouwagi,
    t.zabudowany, t.sred_zabud, t.las, t.sad, t.park, t.pole_orne, t.laka, t.nieuzytek,
    t.woda, t.torf, t.bagno, t.prywatny, t.spoleczny,
    t.przemyslowy, t.uwagi as tuwagi,
    w.wartosc, w.inwentaryzacja, w.wykopaliska, w.interwencja, w.uwagi as wuwagi,
    z.wystepowanie, z.przyczyna_ludzie, z.przyczyna_natura, 
    z.uzytkownik_spoleczny, z.uzytkownik_prywatny,  z.czas, z.uwagi as zuwagi, 
    e.eksponowany, e.kraw_stoki, e.sfaldowania_cyple, e.cyple_wybitne, e.waly_garby,
    e.wyniesienia_okrezne, e.osloniety, e.podst_stoku, e.doliny_niecki, e.kotlinki_zagleb,
    e.jaskinie, e.rozmiar, e.stopien, e.kierunek, e.uwagi as euwagi,
    gd.luzna, gd.zwiezla, gd.torf_bag as ug_torfbag, gd.uwagi as specjalistyczne, kamienistosc,
    a.nr_krz, a.data_krz, a.park as park_kult, a.plan as plan_zp, a.magazyn, a.nr_inwentarza,
    k.nazwa_lok, k.dalsze_losy, k.dzieje_badan as historia, k.metryka_hist, k.literatura,
    k.dzialka_geodezyjna, k.egb, k.chronologia, k.konsultant, k.uwagi as kuwagi,
    s.id as stanowisko
from stanowiska s 
    left outer join fizgeo_dane f on s.id = f.stanowisko
    left outer join obszar_dane o on s.id = o.stanowisko
    left outer join teren_dane t on s.id = t.stanowisko
    left outer join wnioski w on s.id = w.stanowisko
    left outer join zagrozenia z on s.id = z.stanowisko
    left outer join ekspozycja_dane e on s.id = e.stanowisko
    left outer join gleba_dane gd on s.id = gd.stanowisko 
    left outer join aktualnosci a on s.id = a.stanowisko
    left outer join karty k on s.id = k.stanowisko
    left outer join miejscowosci m on s.miejscowosc = m.id
    left outer join powiaty p on s.powiat = p.id
    left outer join gminy g on s.gmina = g.id
    left outer join wojewodztwa ww on s.wojewodztwo = ww.id
    where s.id=?''' # wspolrzedne bedzie trzeba okreslac osobno za pomoca funkcji qgis
    return con.prep(sql)

def getDane(stmt, ident):
    return stmt.jeden([ident],mkmapa)

def _prepLog(m):
    if m['data'] is not None:
        dt = m['data'][:10]
        m['data'] = '%s/%s/%s'%(dt[8:],dt[5:7],dt[0:4])
    for (k,v) in m.iteritems():
        if v == 'T':
            m[k] = 'x'
        elif v is None or v == 'N':
            m[k] = ''        

def _prepObser(m):
    ob = m.pop('obserwacja',None)
    if ob is None: # ten warunek mozna potem usunac
        print 'brak obserwacji'
    else:
        if ob == 'B':
            m['obs_bez_przeszkod'] = 'x'
        elif ob == 'U':
            m['obs_utrudniona'] = 'x'
    p = m.pop('pole',None)
    if p == 'O':
        m['obs_pole_otwarte'] = 'x'
    elif p == 'Z':
        m['obs_pole_zamkniete'] = 'x'
    nr = m.pop('nasyc_rozklad',None)
    if nr == 'R':
        m['obs_nasyc_rozkl_rownomierne'] = 'x'
    nt = m.pop('nasyc_typ',None)
    if nt == 'J':
        m['nasyc_typ_jednocentr'] = 'x'
    elif nt == 'W':
        m['nasyc_typ_wielocentr'] = 'x'
    gz = m.pop('gestosc_znal',None)
    if gz == 'M':
        m['obs_gest_mala'] = 'x'
    elif gz == 'S':
        m['obs_gest_sre'] = 'x'
    elif gz == 'D':
        m['obs_gest_duza'] = 'x'
    pw = m.pop('powierzchnia')
    if pw < 0.5:
        m['obs_pow_ar1'] = 'x'
    elif pw < 1:
        m['obs_pow_ha05'] = 'x'
    elif pw < 5:
        m['obs_pow_ha1'] = 'x'
    elif pw < 15:
        m['obs_pow_ha5'] = 'x'
    elif pw < 16:
        m['obs_pow_ha15'] = 'x'
    else:
        m['obs_pow_ha15+'] = 'x'
    #print ob,p,nr,nt,gz,pw
    
def _prepZagr(m):
    wy = m.pop('wystepowanie',None)
    zag = u''
    if wy == 'I':
        zag += u'Istnieje\n'
    cz = m.pop('czas',None)
    if cz == 'S':
        zag += u'Stałe\n'
    elif cz == 'D':
        zag+=u'Doraźne\n'
    pr = m.pop('przyczyna_ludzie',None)
    if pr == 'x':
        zag += u'Przyczyna: ludzie\n'
    pr = m.pop('przyczyna_natura',None)
    if pr == 'x':
        zag += u'Przyczyna: natura\n'
    uz = m.pop('uzytkownik_spoleczny',None)
    if uz == 'x':
        zag+= u'Użyt. społ\n'
    uz = m.pop('uzytkownik_prywatny',None)
    if uz == 'x':
        zag+= u'Użyt. pryw\n'
    uw = m.pop('zuwagi',None)
    if uw is not None:
        zag += uw
    m['opis_zagrozenia'] = zag
    
def _prepRodz(m):
    ro = m.pop('rodzaj_badan',None)
    if ro is not None:
        m['rodz_'+ro.lower()] = 'x' 

def _prepTer(m):
    if m['zabudowany'] != 'x' and m['sred_zabud'] != 'x':
        m['niezabudowany'] = 'x'
        
def _prepFk(nr,m):
    opis = u''
    if m['masowy'] != '':
        opis += u'masowy: %s;'%m['masowy']
    if m['wydzielony'] != '':
        opis += u'wydzielone: %s'%m['wydzielony']
    return {'nr%d'%nr:str(nr), 'fun%d'%nr:m['funkcja'], 'kult%d'%nr:m['kultura'], 'chrono%d'%nr:m['chronologia'],
            'opis%d'%nr:opis}

def _prepImg(con, m):
    ps = con.prep('select s.medium from st_media s join media m on s.medium = m.id where s.stanowisko=?')
    r = ps.jeden([m['stanowisko']])
    if r is None:
        return None
    print r[0], m['stanowisko']
    return odczyt(r[0], con)

class Karta(object):
    
    NORM = QFont('Times',8,QFont.Normal)
    BOLD = QFont('Times',6,QFont.DemiBold)
    
    def __init__(self,tab,kwsp):
        self._tab = tab
        self._kwsp = kwsp
        
    def scal(self,x,y,szer,wys):
        self._tab.mergeCells(y,x,wys,szer)
    
    def setTxt(self, x, y, txt, font=NORM, tlo=Qt.white, wyr=QTextCharFormat.AlignNormal):
        kom = self._tab.cellAt(y, x)
        fmt = kom.format()
        fmt.setFont(font)
        fmt.setBackground(tlo)
        fmt.setVerticalAlignment(wyr)
        kom.setFormat(fmt)
        kom.firstCursorPosition().insertText(txt)
    
    def setImg(self, x, y, qimg):
        print 'set img'
        dx,dy = qimg.dotsPerMeterX(), qimg.dotsPerMeterY()
        nw = (12 * dx) / 100 # nowa szerokosc wg wzor szer w cm / (100 / dx )
        nh = (12 * dy) / 100
        qimg = qimg.scaled(nw,nh,Qt.KeepAspectRatio)
        self._tab.cellAt(y, x).firstCursorPosition().insertImage(qimg)
    
    def setDane(self,md):
        for (k,v) in md.iteritems():
            self[k] = v
        
    def __setitem__(self,k,v):
        if not self._kwsp.has_key(k):
            return
        elif v is None:
            return
        if isinstance(v,unicode):
            w = self._kwsp[k]
            self.setTxt(w[0],w[1],v)
        elif isinstance(v,(str,int,float)):
            w = self._kwsp[k]
            self.setTxt(w[0],w[1],unicode(v))
        elif isinstance(v,QImage):
            w = self._kwsp[k]
            self.setImg(w[0],w[1],v)
        else:
            raise Exception('nieprawidlowy typ '+str(type(v)))

class HtmlFormat(QTextTableFormat):
    
    def __init__(self):
        QTextTableFormat.__init__(self)
        self.setPageBreakPolicy(QTextFormat.PageBreak_AlwaysAfter)
        self.setWidth(QTextLength(QTextLength.PercentageLength,100))
        self.setHeight(QTextLength(QTextLength.PercentageLength,100))
        self.setCellPadding(1)
        self.setBorderStyle(QTextFrameFormat.BorderStyle_Solid) 

class Schemat(object):
    
    def __init__(self, plik):
        # definicja rozmieszczenia komorek w tabeli.
        # kazdy element listy to krotka (x, y, szer, wys, wartosc)
        # punkt 0,0 - gorny lewy naroznik tabeli
        # puste pole 'wartosc' oznacza pole do edycji, ktore mozna uzupelnic,
        # przez wskazanie na karcie klucza
        self._pola = []
        # klucze pol do edycji
        self._wsp = {}
        sp = open(plik, 'r')
        for w in sp.readlines():
            if w.startswith('#'):
                continue
            tw = w.split(';')
            if len(tw) == 1:
                continue
            if 1 <  len(tw) < 6:
                sp.close()
                raise Exception('zly schemat') # nieprawidlowy schemat
            #print tw
            x,y,s,w = int(tw[0]), int(tw[1]), int(tw[2]), int(tw[3]) 
            v = tw[4].strip().decode('utf-8')
            if v.startswith('k:'):
                k = v[2:]
                if self._wsp.has_key(k):
                    sp.close()
                    raise Exception('zly schemat') # powtorzenie klucza
                self._wsp[k] = (x,y)
                self._pola.append((x,y,s,w,None))
            else:
                self._pola.append((x,y,s,w,v))
        sp.close()
        self.hf = HtmlFormat()
        
    def karta(self,kursor):
        k = Karta(kursor.insertTable(36,60,self.hf),self._wsp)
        for p in self._pola:
            k.scal(p[0],p[1],p[2],p[3])
            if p[4] is not None:
                k.setTxt(p[0],p[1],p[4],tlo=Qt.yellow,font=Karta.BOLD)
        return k

class GeneratorKeza(object):   
    
    pstr = Schemat(abspath(__file__+'/../../keza/astr.txt'))
    dstr = Schemat(abspath(__file__+'/../../keza/bstr.txt'))
    
    def __init__(self, con):
        self._con = con
        self._daneStmt = prepSt(con)
        self._owyk, self._jwyk, self._fwyk = okrWykaz(con), jedWykaz(con), funWykaz(con) 
        self._doc = QTextDocument()
        self._txtCur = QTextCursor(self._doc)
        self._klicz = 0
    
    def zapisz(self, plik):
        dev = QPrinter()
        dev.setOutputFormat(QPrinter.PdfFormat)
        dev.setOrientation(QPrinter.Landscape)
        dev.setOutputFileName(plik)
        dev.setPageMargins(5,5,5,5,QPrinter.Millimeter)
        self._doc.print_(dev)
        return self._klicz
    
    def dodajKarte(self, stid, wsp={}):
        pkz = self.pstr.karta(self._txtCur)
        md = getDane(self._daneStmt, stid)
        _prepLog(md)
        _prepObser(md)
        _prepZagr(md)
        _prepRodz(md)
        _prepTer(md)
        pkz.setDane(md)
        wf = WykazFaktow(str(md['stanowisko']), self._con, self._owyk, self._jwyk, self._fwyk)
        for i in range(len(wf)):
            if i < 7:
                f = _prepFk(i+1,wf.mapa(i))
                pkz.setDane(f)
        self._txtCur.movePosition(QTextCursor.End)
        dkz = self.dstr.karta(self._txtCur)
        img = _prepImg(self._con,md)
        if img is not None:
            dkz['mapa_img'] = img
        md['wsp_x'] = str(wsp['x'])
        md['wsp_y'] = str(wsp['y'])
        dkz.setDane(md)
        self._txtCur.movePosition(QTextCursor.End)
        self._klicz += 1