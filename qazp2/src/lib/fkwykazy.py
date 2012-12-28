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
#
# Wykazy uzywane do edytowania faktow kulturowych

from functools import partial

def mapaFk(r,t):
        return dict(zip(t,r))

class KodyWykaz(object):

    def __init__(self,con,tab,atr=['kod','nazwa','skrot']):
        self._TAB = tab
        ps = con.prep('select '+','.join(atr)+' from '+self._TAB+' order by nazwa')
        self._kody = {}
        for tk in ps.wszystkie(f=partial(mapaFk,t=atr)):
            self._kody[tk['kod']] = tk
    
    def widok(self, k):
        if k is None:
            return None
        r = self._kody.get(k,None)
        if r is None:
            raise Exception('Nie ma klucza w tabeli'+self._TAB+' '+str(k))
        return self._kody[k]['skrot']
    
    def listaKat(self,pref):
        for (k,v) in self._kody.iteritems():
            if k is not None and k.startswith(pref) and v['nazwa'] is not None:
                yield (v['kod'], v['nazwa'])
                
    def nazwa(self,k):
        r = self._kody.get(k,None)
        if r is None:
            raise Exception('Nie ma klucza w tabeli '+str(k))
        return r['nazwa']

class WykazFaktow(object):
    
    FAKTY_ATR = ['id','okresa','okresb','okr_relacja','okr_pewnosc','jeda','jedb',
                   'jed_relacja' ,'jed_pewnosc', 'funkcja', 'fun_pewnosc',
                   'masowy', 'wydzielony' ]
    
    def __init__(self, st, con, owyk, jwyk, fwyk):
        self._ow, self._jw, self._fw = owyk, jwyk, fwyk
        self._selStmt = con.prep('select '+','.join(self.FAKTY_ATR)+' from fakty where stanowisko='+st)
        self._updtStmt = con.prep('update fakty set okresa = :okresa, okresb = :okresb, okr_relacja=:okr_relacja,' \
                                  'okr_pewnosc=:okr_pewnosc, jeda=:jeda, jedb = :jedb, jed_relacja=:jed_relacja,' \
                                  ' jed_pewnosc=:jed_pewnosc,funkcja=:funkcja, fun_pewnosc=:fun_pewnosc,' \
                                  ' masowy=:masowy, wydzielony=:wydzielony' \
                                  ' where id=:id and stanowisko='+str(st))
        self._insStmt = con.prep('insert into fakty values(:id,'+str(st)+', :okresa, :okresb, '\
                                 ':okr_relacja, :okr_pewnosc, :jeda, :jedb, :jed_relacja, :jed_pewnosc,'\
                                 ' :funkcja, :fun_pewnosc, :masowy, :wydzielony)')
        self._delStmt = con.prep('delete from fakty where id=:id and stanowisko='+str(st))
        self._mxFk = con.prep('select coalesce(max(id),0) from fakty')
        self._mf = partial(mapaFk,t=self.FAKTY_ATR) # funkcja do tworzenia slowika gdzie kluczami sa wartosci tabeli FAKTY_ATR
        self.odswiez()
    
    def odswiez(self):
        self._fk = self._selStmt.wszystkie(f=self._mf)
        
    def __len__(self):
        return len(self._fk)
    
    def get(self,i, k, d=None):
        if i == len(self._fk):
            return d
        f= self._fk[i].get(k)
        if f is None:
            return d
        return f
    
    def setMapa(self,i,mapa):
        for (k,v) in mapa.iteritems():
            self.setWartosc(i,k,v)
    
    def setWartosc(self,i,k,v):
        if i == len(self._fk):
            self._fk.append(dict([(a,None) for a in self.FAKTY_ATR]))
            self._fk[i]['okr_pewnosc'] = 1
            self._fk[i]['jed_pewnosc'] = 1
            self._fk[i]['fun_pewnosc'] = 1
        self._fk[i][k] = v
    
    def prepParams(self,m):
        if m['okresa'] == '':
            m['okresa'] = None
        if m['okresb'] == '' or (m['okr_relacja'] is None or m['okr_relacja'] == ''):
            m['okresb'] = None
            m['okr_relacja'] = None
        if round(float(m['okr_pewnosc']),2) == 0:
            m['okresa'] = None
            m['okresb'] = None
            m['okr_relacja'] = None
            m['okr_pewnosc'] = 0
        if m['jeda'] == '':
            m['jeda'] = None
        if m['jedb'] == '' or (m['jed_relacja'] is None or m['jed_relacja'] == ''):
            m['jedb'] = None
            m['jed_relacja'] = None
        if round(float(m['jed_pewnosc']),2) == 0:
            m['jed_pewnosc'] = 0
            m['jeda'] = None
            m['jedb'] = None
            m['jed_relacja'] = None
        if m['funkcja'] == '':
            m['funkcja'] = None
        if round(float(m['fun_pewnosc']),2) == 0:
            m['funkcja'] = None
            m['fun_pewnosc'] = 0
        return m
    
    def usun(self,i):
        if i >= len(self._fk):
            pass
        f = self._fk[i]
        if f['id'] < 0:
            self._fk.pop(i)
        elif f['id'] > 0:
            if self._delStmt.wykonaj(f,zatwierdz=False) != 1:
                raise Exception('Nieudane usuniecie')
        self.odswiez()
    
    def zmien(self,i):
        if i >= len(self._fk):
            pass
        f = self._fk[i]
        if f['id'] < 0:
            f['id'] = self._mxFk.jeden()[0]+1
            r = self._insStmt.wykonaj(params=self.prepParams(f),zatwierdz=False)
            if r != 1:
                raise Exception('Nieudane wstawienie nowego faktu')
        elif f['id'] > 0:
            r = self._updtStmt.wykonaj(params=self.prepParams(f),zatwierdz=False)
            if r != 1:
                raise Exception('Nieudana zmiana faktu')
        self.odswiez()
        
    def jedWidok(self, i):
        f = self._fk[i]
        nja, njb = self._jw.widok(f['jeda']), self._jw.widok(f['jedb'])
        widok = ''
        if f['jed_pewnosc'] is not None and 0 < float(f['jed_pewnosc']) < 1:
            widok = '?'
        if njb is not None and nja is not None:
            if f['jed_relacja'] == 'Z':
                widok += nja+'-'+njb
            elif f['jed_relacja'] == 'P':
                widok += nja+'/'+njb
        elif nja is not None:
            widok += nja
        return widok
        
    def okrWidok(self, i):
        f = self._fk[i]
        noa, nob = self._ow.widok(f.get('okresa')), self._ow.widok(f.get('okresb'))
        widok = ''
        if f['okr_pewnosc'] is not None and 0 < float(f['okr_pewnosc']) < 1:
            widok = '?'
        if nob is not None and noa is not None:
            if f['okr_relacja'] == 'Z':
                widok += noa+'-'+nob
            elif f['okr_relacja'] == 'P':
                widok += noa+'/'+nob
        elif noa is not None:
            widok += noa
        return widok
    
    def funWidok(self, i):
        f = self._fk[i]
        widok = ''
        if f['fun_pewnosc'] is not None and 0 < float(f.get('fun_pewnosc','1')) < 1:
            widok = '?'
        nf = self._fw.widok(f.get('funkcja'))
        if nf is not None:
            widok += self._fw.widok(f.get('funkcja'))
        return widok
    
    def mapa(self,r):
        return {'chronologia':self.widok(r,0), 'kultura':self.widok(r,1), 'funkcja':self.widok(r,2), 'masowy':self.widok(r,3),
                    'wydzielony':self.widok(r,4)}
    
    def widok(self, r, c):
        if c == 0:
            return self.okrWidok(r)
        elif c == 1:
            return self.jedWidok(r)
        elif c == 2:
            return self.funWidok(r)
        elif c == 3:
            return self._fk[r]['masowy']
        elif c == 4:
            return self._fk[r]['wydzielony']

def funWykaz(con):
    return KodyWykaz(con,'funkcje')

def jedWykaz(con):
    return KodyWykaz(con,'jednostki')

def okrWykaz(con):
    return KodyWykaz(con,'okresy_dziejow') 