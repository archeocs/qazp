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
                'park_kult', 'plan_zp', 'magazyn', 'nr_inwentarza', 'wlasciciel', 
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
    a.nr_krz, a.data_krz, a.park as park_kult, a.plan as plan_zp, a.magazyn, a.nr_inwentarza, a.wlasciciel,
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
    if pw <= 0.01:
        m['obs_pow_ar1'] = 'x'
    elif pw <= 0.5:
        m['obs_pow_ha05'] = 'x'
    elif pw <= 1:
        m['obs_pow_ha1'] = 'x'
    elif pw <= 5:
        m['obs_pow_ha5'] = 'x'
    elif pw <= 15:
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
    if m['masowy'] is not None and m['masowy'] != '':
        opis += u'masowy: %s;'%m['masowy']
    if m['wydzielony'] is not None and m['wydzielony'] != '':
        opis += u'wydzielone: %s'%m['wydzielony']
    return {'nr%d'%nr:str(nr), 'fun%d'%nr:m['funkcja'], 'kult%d'%nr:m['kultura'], 'chrono%d'%nr:m['chronologia'],
            'opis%d'%nr:opis}

def _prepAkt(m):
    if m['wlasciciel'] is None or m['wlasciciel'].strip() == '':
        if m['prywatny'] == 'x':
            m['wlasciciel'] = 'PRYWATNY'
        elif m['spoleczny'] == 'x':
            m['wlasciciel'] = u'SPOŁECZNY'
        
def _prepImg(con, m):
    ps = con.prep('select s.medium from st_media s join media m on s.medium = m.id where s.stanowisko=?')
    r = ps.jeden([m['stanowisko']])
    if r is None:
        return None
    print r[0], m['stanowisko']
    return odczyt(r[0], con)

class Schemat2(object):
    
    NORM = QFont('Times',8,QFont.Normal)
    BOLD = QFont('Times',7,QFont.DemiBold)
    
    def __init__(self, plik):
        self._pola = []
        sp = open(plik, 'r')
        for (wi, w) in enumerate(sp.readlines()):
            if w.startswith('#'):
                continue
            tw = w.split(';')
            if len(tw) == 1:
                continue
            if 1 <  len(tw) < 6:
                sp.close()
                raise Exception('zly schemat linia '+str(wi)) # nieprawidlowy schemat
            x,y,s,w = int(tw[0]), int(tw[1]), int(tw[2]), int(tw[3]) 
            v = tw[4].strip().decode('utf-8')
            self._pola.append((x, y, s, w, v))
        sp.close()
   
    def mkrect(self, kw, kh, p):
        rx, ry = kw * p[0], kh * p[1]
        rw, rh = kw * p[2], kh * p[3]
        return QRect(rx, ry, rw, rh)
    
    def druk(self, pt, dane={}):
        kw, kh = pt.device().width()/60, pt.device().height()/36    
        etb = QBrush(Qt.yellow)
        wab = QBrush(Qt.white)
        for p in self._pola:
            if not p[4].startswith('k:'): # etykieta
                pt.setBrush(etb)
                r = self.mkrect(kw, kh, p)
                pt.drawRect(r)
                pt.setFont(self.BOLD)
                tr = QRectF(r.x()+3, r.y()+3, r.width()-3, r.height()-3)
                topt = QTextOption(Qt.AlignCenter)
                topt.setWrapMode(QTextOption.WordWrap)
                pt.drawText(tr, p[4], topt) 
            else: # wartosc
                pt.setBrush(wab)
                r = self.mkrect(kw, kh, p)
                pt.drawRect(r)
                k = p[4][2:]
                if dane.has_key(k) and dane[k] is not None:
                    pt.setFont(self.NORM)
                    tr = QRectF(r.x()+2, r.y()+2, r.width()-2, r.height()-2)
                    topt = QTextOption(Qt.AlignCenter)
                    topt.setWrapMode(QTextOption.WordWrap)
                    if not isinstance(dane[k], QImage):
                        pt.drawText(tr, dane[k], topt)
                    else:
                        pt.drawImage(tr, dane[k], tr)

class KezaDruk(object):
    
    def __init__(self, con):
        self._con = con
        #self._sts = sts
        self._daneStmt = prepSt(con)
        self._owyk, self._jwyk, self._fwyk = okrWykaz(con), jedWykaz(con), funWykaz(con) 
    
    def _prepDane(self, st):
        md = getDane(self._daneStmt, st)
        _prepLog(md)
        _prepObser(md)
        _prepZagr(md)
        _prepRodz(md)
        _prepTer(md)
        _prepAkt(md)
        md['mapa_img'] = _prepImg(self._con, md)
        wf = WykazFaktow(str(md['stanowisko']), self._con, self._owyk, self._jwyk, self._fwyk)
        for i in range(len(wf)):
            if i < 7:
                for (k, v) in _prepFk(i+1,wf.mapa(i)).iteritems():
                    md[k] = v
        md['historia'] = md['historia']+' '+md['uwagi']
        return md
    
    def drukuj(self, plik, sts, postep):
        dev = QPrinter()
        dev.setOutputFormat(QPrinter.PdfFormat)
        dev.setOrientation(QPrinter.Landscape)
        dev.setOutputFileName(plik)
        dev.setPaperSize(QPrinter.A4)
        dev.setPageMargins(5,5,5,5,QPrinter.Millimeter)
        pt = QPainter()
        pt.begin(dev)
        pt.setPen(QPen(Qt.black, 1))
        astr = Schemat2(abspath(__file__+'/../../keza/astr.txt'))
        bstr = Schemat2(abspath(__file__+'/../../keza/bstr.txt'))
        c = 0
        for s in sts:
            md = self._prepDane(s[0])
            md['wsp_x'] = str(s[3])
            md['wsp_y'] = str(s[4])
            c += 1
            postep.setValue(c)
            postep.setLabelText(u'Stanowisko %s/%s'%(s[1], s[2]))
            astr.druk(pt, md)
            dev.newPage()
            bstr.druk(pt, md)
            if c < len(sts):
                dev.newPage()
        postep.setValue(len(sts))
        pt.end()
