'''
Created on Jul 8, 2011

@author: milosz
'''
# dane z bazy danych

from slow_def import Slow
from teren_def import Teren
from lokal_def import Lokalizacja
from poloz_def import Polozenie
from eksp_def import Ekspozycja
from stan_def import Stanowisko
from fakt_def import Fakt
from obszar_def import Obszar
from wnioski_def import Wnioski
from zagroz_def import Zagrozenie

class Wiersz:
    
    arkusz = None
    nr_ark = None
    data = None
    
    def __init__(self,w):
        self.arkusz = str(w[0])
        self.nr_ark = str(w[1])
        self.data = str(w[2])
        
class DaneAzp:
    
    slista = []
    
    def set_polaczenie(self,p):
        self.p = p
        
    def kryteria(self):
        #krlista = 
        #return self.p.get_kryteria()
        return [Wiersz(k) for k in self.p.get_kryteria()]
        
    def lista_ark(self):
        return self.p.get_arkusze()
        
    def lista_nrark(self,a):
        return self.p.get_nrark(a)
        
    def stanowiska(self,a,n=-1): #a - arkusz, n - nr arkusz
        if n == -1:
            return [Stanowisko(s) for s in self.p.get_stanowiska(" where arkusz = '%s'"%a)]
        else:
            return [Stanowisko(s) for s in self.p.get_stanowiska(" where arkusz = '%s' and nr_arkusz = '%s'"%(a,n))]
            
    def miasta(self):
        mt = self.p.wykonaj('select sid,nazwa from miasta_slo order by nazwa')
        return Slow(mt,self.p,Slow.MIASTA)
        
    def powiaty(self):
        pt = self.p.wykonaj('select sid,nazwa from powiaty_slo order by nazwa') # nalezy ujednolicic nazewnictwo tabel !!!!!
        return Slow(pt,self.p,Slow.POWIATY)
        
    def wojewod(self):
        wt = self.p.wykonaj('select sid,nazwa from wojewodztwa_slo order by nazwa') # nalezy ujednolicic nazewnictwo tabel !!!!!
        return Slow(wt,self.p,Slow.WOJEWODZ)
        
    def gminy(self):
        gt = self.p.wykonaj('select sid,nazwa from gminy_slo order by nazwa')
        return Slow(gt,self.p,Slow.GMINY)
        
    def kultury(self):
        kt = self.p.wykonaj('select sid,nazwa from kultury_slo order by nazwa')
        return Slow(kt,self.p,Slow.KULTURY)
        
    def funkcje(self):
        ft = self.p.wykonaj('select sid,nazwa from funkcje_slo order by nazwa')
        return Slow(ft,self.p,Slow.FUNKCJE)
        
    def epoki(self):
        et = self.p.wykonaj('select sid,nazwa from epoki_slo order by nazwa')
        return Slow(et,self.p,Slow.EPOKI)
        
    def lokalizacja(self,stan):
        if stan.lokalizacja is None:
            return Lokalizacja(stan,self.p)
        else:
            return Lokalizacja(stan,self.p,self.p.lokal_info(stan.lokalizacja))
    
    def znajdz_lokal(self,stan,ark,nr):
        lid = self.p.lokal_lid(ark,nr)
        if lid is not None:
            return Lokalizacja(stan,self.p,self.p.lokal_info(lid))
        else:
            return None        
            
    def ekspozycja(self,stan):
        return Ekspozycja(stan,self.p,self.p.eksp_info(stan))
        
    def teren(self,stan):
        return Teren(stan,self.p,self.p.teren_info(stan))
        
    def polozenie(self,stan):
        return Polozenie(stan,self.p,self.p.polozenie_info(stan))
    
    def obszar(self,stan):
        return Obszar(stan,self.p,self.p.obszar_info(stan))
    
    def wnioski(self,stan):
        return Wnioski(stan,self.p,self.p.wnioski_info(stan))
    
    def zagrozenia(self,stan):
        return Zagrozenie(stan,self.p,self.p.zagroz_info(stan))
        
    def fakty(self,stan):
        return map(lambda x: Fakt(stan,self.p,x), self.p.fakty_info(stan))
        
    def nowy_fakt(self,stan):
        return Fakt(stan,self.p)